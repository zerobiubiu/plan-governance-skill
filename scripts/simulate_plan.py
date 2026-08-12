#!/usr/bin/env python3
"""执行基础 S0 Plan Simulation：依赖、输入输出和执行顺序静态演练。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def simulate(plan: dict[str, Any]) -> dict[str, Any]:
    """按可满足 hard dependency 的顺序模拟 Task，并返回 Trace/Findings。"""
    tasks = {t.get("id"): t for t in plan.get("tasks", []) if t.get("id")}
    pending = set(tasks)
    done: set[str] = set()
    outputs: set[str] = set()
    trace: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []

    while pending:
        progressed = False
        for tid in sorted(list(pending)):
            task = tasks[tid]
            deps = {str(x) for x in task.get("dependencies", {}).get("hard", [])}
            if not deps.issubset(done):
                continue

            required_outputs = {str(x) for x in task.get("inputs", {}).get("outputs", [])}
            missing = sorted(required_outputs - outputs)
            if missing:
                findings.append({"rule":"SIM001","severity":"BLOCKER","task":tid,"message":f"缺少输入 Output: {', '.join(missing)}"})
                trace.append({"task":tid,"state":"BLOCKED","missing_outputs":missing})
                pending.remove(tid)
                progressed = True
                continue

            projected = []
            for item in task.get("outputs", []):
                oid = item.get("id") if isinstance(item, dict) else item
                if oid:
                    oid = str(oid)
                    outputs.add(oid)
                    projected.append({"id":oid,"state":"PROJECTED"})
            trace.append({"task":tid,"state":"SIMULATED","outputs":projected})
            done.add(tid)
            pending.remove(tid)
            progressed = True

        if not progressed:
            for tid in sorted(pending):
                deps = tasks[tid].get("dependencies", {}).get("hard", [])
                findings.append({"rule":"SIM001","severity":"BLOCKER","task":tid,"message":f"依赖无法满足: {deps}"})
                trace.append({"task":tid,"state":"BLOCKED","dependencies":deps})
            break

    status = "COMPLETE" if not findings else "BLOCKED"
    return {"status":status,"trace":trace,"findings":findings,"coverage":{"tasks_simulated":len(done),"tasks_total":len(tasks)}}


def main() -> int:
    """CLI 入口。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    result = simulate(plan)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
