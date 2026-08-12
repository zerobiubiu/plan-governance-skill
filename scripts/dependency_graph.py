#!/usr/bin/env python3
"""从 Plan IR 输出 Task hard dependency 的 DOT 图。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_dot(plan: dict) -> str:
    """把 Plan tasks/dependencies 转换为 Graphviz DOT 文本。"""
    lines = ["digraph plan {", "  rankdir=LR;"]
    tasks = {t.get("id"): t for t in plan.get("tasks", []) if t.get("id")}
    for tid, task in tasks.items():
        title = str(task.get("title", tid)).replace('"', '\\"')
        lines.append(f'  "{tid}" [label="{tid}\\n{title}"];')
    for tid, task in tasks.items():
        for dep in task.get("dependencies", {}).get("hard", []):
            if dep in tasks:
                lines.append(f'  "{dep}" -> "{tid}";')
    lines.append("}")
    return "\n".join(lines)


def main() -> int:
    """CLI 入口。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    dot = build_dot(plan)
    if args.output:
        args.output.write_text(dot, encoding="utf-8")
    else:
        print(dot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
