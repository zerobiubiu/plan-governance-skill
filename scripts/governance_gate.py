#!/usr/bin/env python3
"""根据 Plan IR 的关键治理状态判断是否满足基础 Execution Ready Gate。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ACTIVE_BLOCKING_STATES = {"OPEN","TRIAGED","CONFIRMED","FIX_PLANNED","FIXED_UNVERIFIED","REVERIFYING","REOPENED","INVESTIGATE"}


def gate(plan: dict[str, Any]) -> dict[str, Any]:
    """执行基础 Hard Gate；仅判断结构化状态，不替代语义 Auditor。"""
    failures: list[dict[str, str]] = []

    for issue in plan.get("issues", []):
        if issue.get("severity") == "BLOCKER" and issue.get("status") in ACTIVE_BLOCKING_STATES:
            failures.append({"gate":"blocking_issue","message":f"存在活动 Blocker: {issue.get('id')}"})

    for unknown in plan.get("unknowns", []):
        if unknown.get("class") == "planning_blocker" and unknown.get("status", "open") not in {"resolved","closed"}:
            failures.append({"gate":"planning_unknown","message":f"Planning blocker 未解决: {unknown.get('id')}"})

    requirements = {r.get("id") for r in plan.get("requirements", []) if r.get("priority") == "mandatory"}
    covered = set()
    for task in plan.get("tasks", []):
        covered.update(task.get("covers", {}).get("requirements", []))
    for rid in sorted(x for x in requirements - covered if x):
        failures.append({"gate":"requirement_coverage","message":f"Mandatory Requirement 未覆盖: {rid}"})

    gov = plan.get("governance", {})
    if gov.get("required_independent_validation") and gov.get("independent_validation_status") not in {"passed","approved"}:
        failures.append({"gate":"independent_validation","message":"要求独立验证但尚未通过"})
    if gov.get("simulation_required") and gov.get("simulation_status") != "complete":
        failures.append({"gate":"simulation","message":"要求 Simulation 但尚未完成"})

    return {"ready":not failures,"failures":failures}


def main() -> int:
    """CLI 入口。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    result = gate(plan)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
