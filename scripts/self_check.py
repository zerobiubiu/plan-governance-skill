#!/usr/bin/env python3
"""检查 Skill 文件、JSON 配置和示例脚本是否可用。"""

from __future__ import annotations

import json
import py_compile
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED = [
    "SKILL.md",
    "AGENTS.md",
    "core/invariants.md",
    "core/convergence.md",
    "context/protocol.md",
    "authority/envelope.md",
    "rules/core-rules.json",
    "schemas/plan-ir.schema.json",
    "examples/sample-plan.json",
]


def main() -> int:
    """运行静态自检与示例 Plan Lint/Simulation。"""
    failures: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            failures.append(f"缺少必要文件: {rel}")

    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            failures.append(f"JSON 无效 {path.relative_to(ROOT)}: {exc}")

    for path in (ROOT / "scripts").glob("*.py"):
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"Python 编译失败 {path.name}: {exc}")

    sample = ROOT / "examples" / "sample-plan.json"
    lint = subprocess.run([sys.executable, str(ROOT / "scripts" / "plan_lint.py"), str(sample)], capture_output=True, text=True)
    if lint.returncode != 0:
        failures.append(f"示例 Plan lint 失败:\n{lint.stdout}\n{lint.stderr}")

    approval_sample = ROOT / "examples" / "sample-approval.json"
    lint_apv = subprocess.run([sys.executable, str(ROOT / "scripts" / "plan_lint.py"), str(approval_sample)], capture_output=True, text=True)
    if lint_apv.returncode != 0:
        failures.append(f"示例 Approval Plan lint 失败:\n{lint_apv.stdout}\n{lint_apv.stderr}")

    gate = subprocess.run([sys.executable, str(ROOT / "scripts" / "governance_gate.py"), str(sample)], capture_output=True, text=True)
    if gate.returncode != 0:
        failures.append(f"示例 Plan governance gate 失败:\n{gate.stdout}\n{gate.stderr}")

    sim = subprocess.run([sys.executable, str(ROOT / "scripts" / "simulate_plan.py"), str(sample)], capture_output=True, text=True)
    if sim.returncode != 0:
        failures.append(f"示例 Plan simulation 失败:\n{sim.stdout}\n{sim.stderr}")

    if failures:
        print("SELF CHECK FAILED")
        for item in failures:
            print(f"- {item}")
        return 1

    print("SELF CHECK PASSED")
    print(f"Skill root: {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
