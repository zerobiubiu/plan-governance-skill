#!/usr/bin/env python3
"""对 Plan Governance JSON IR 执行核心确定性检查。"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


BLOCKING_ISSUE_STATES = {
    "OPEN",
    "TRIAGED",
    "CONFIRMED",
    "FIX_PLANNED",
    "FIXED_UNVERIFIED",
    "REVERIFYING",
    "REOPENED",
}


def load_json(path: Path) -> dict[str, Any]:
    """读取 JSON 文件并返回对象；根对象不是字典时抛出 ValueError。"""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Plan IR 根对象必须是 JSON object")
    return data


def finding(rule: str, message: str, severity: str = "BLOCKER", affected: list[str] | None = None) -> dict[str, Any]:
    """创建统一的确定性 Finding。"""
    return {
        "rule": rule,
        "severity": severity,
        "message": message,
        "affected": affected or [],
    }


def task_map(plan: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    """建立 Task ID 映射，并返回重复 ID Finding。"""
    result: dict[str, dict[str, Any]] = {}
    findings: list[dict[str, Any]] = []
    for task in plan.get("tasks", []):
        tid = task.get("id")
        if not tid:
            findings.append(finding("SCH002", "存在缺少 id 的 Task"))
            continue
        if tid in result:
            findings.append(finding("SCH001", f"Task ID 重复: {tid}", affected=[tid]))
        result[tid] = task
    return result, findings


def check_requirements(plan: dict[str, Any], tasks: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """检查 mandatory requirement 是否至少被一个 Task 声明覆盖。"""
    covered: set[str] = set()
    for task in tasks.values():
        covers = task.get("covers", {}).get("requirements", [])
        covered.update(str(x) for x in covers)
    out = []
    for req in plan.get("requirements", []):
        rid = req.get("id")
        if req.get("priority") == "mandatory" and rid not in covered:
            out.append(finding("REQ001", f"Mandatory Requirement 未被任务覆盖: {rid}", affected=[str(rid)]))
    return out


def check_dependencies(tasks: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """检查依赖引用与依赖环。"""
    findings: list[dict[str, Any]] = []
    graph: dict[str, set[str]] = {tid: set() for tid in tasks}
    indegree = defaultdict(int)

    for tid, task in tasks.items():
        hard = task.get("dependencies", {}).get("hard", [])
        for dep in hard:
            dep = str(dep)
            if dep not in tasks:
                findings.append(finding("DEP001", f"{tid} 依赖不存在的 Task: {dep}", affected=[tid, dep]))
                continue
            if tid not in graph[dep]:
                graph[dep].add(tid)
                indegree[tid] += 1

    q = deque(tid for tid in tasks if indegree[tid] == 0)
    visited = 0
    while q:
        cur = q.popleft()
        visited += 1
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)
    if visited != len(tasks):
        findings.append(finding("DEP002", "Task hard dependency 存在循环"))
    return findings


def collect_outputs(tasks: dict[str, dict[str, Any]]) -> dict[str, str]:
    """建立 Output ID 到生产 Task 的映射。"""
    outputs: dict[str, str] = {}
    for tid, task in tasks.items():
        for output in task.get("outputs", []):
            oid = output.get("id") if isinstance(output, dict) else output
            if oid:
                outputs[str(oid)] = tid
    return outputs


def check_dataflow(tasks: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """检查 Task 输入引用的 Output 是否存在生产者。"""
    outputs = collect_outputs(tasks)
    findings: list[dict[str, Any]] = []
    for tid, task in tasks.items():
        for oid in task.get("inputs", {}).get("outputs", []):
            oid = str(oid)
            if oid not in outputs:
                findings.append(finding("DATA001", f"{tid} 输入 {oid} 没有生产者", affected=[tid, oid]))
    return findings


def check_evidence(plan: dict[str, Any]) -> list[dict[str, Any]]:
    """检查已验证 Fact 是否至少有 Evidence 引用。"""
    findings = []
    for fact in plan.get("facts", []):
        if fact.get("status") == "verified" and not fact.get("evidence"):
            fid = str(fact.get("id", "<unknown>"))
            findings.append(finding("EVD001", f"Verified Fact 缺少 Evidence: {fid}", affected=[fid]))
    return findings


def check_unknowns(plan: dict[str, Any]) -> list[dict[str, Any]]:
    """检查 planning blocker Unknown。"""
    findings = []
    for item in plan.get("unknowns", []):
        if item.get("class") == "planning_blocker" and item.get("status", "open") not in {"resolved", "closed"}:
            uid = str(item.get("id", "<unknown>"))
            findings.append(finding("UNK002", f"Planning Blocker Unknown 未解决: {uid}", affected=[uid]))
    return findings


def check_validation(tasks: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """检查 implementation/migration/deployment 等关键执行 Task 是否有验证。"""
    critical_types = {"implementation", "migration", "deployment", "rollback"}
    findings = []
    for tid, task in tasks.items():
        if task.get("task_type") in critical_types and not task.get("validation"):
            findings.append(finding("VAL001", f"关键任务没有 validation: {tid}", affected=[tid]))
    return findings


def check_runtime(plan: dict[str, Any]) -> list[dict[str, Any]]:
    """检查 Execution batch 的并发数量和禁止子代理并行策略。"""
    runtime = plan.get("runtime", {})
    max_parallel = runtime.get("max_parallel_agents")
    parallel_subagents = runtime.get("parallel_subagents", True)
    findings = []
    for batch in plan.get("execution", {}).get("batches", []):
        tasks = batch.get("tasks", [])
        if batch.get("mode") == "parallel":
            if isinstance(max_parallel, int) and len(tasks) > max_parallel:
                findings.append(finding("AGT002", f"Batch {batch.get('id')} 并发任务数 {len(tasks)} 超过限制 {max_parallel}", affected=[str(batch.get("id"))]))
            if parallel_subagents is False:
                findings.append(finding("AGT003", f"Runtime 禁止子代理并行，但 Batch {batch.get('id')} 被标记为 parallel", affected=[str(batch.get("id"))]))
    return findings


def check_resource_conflicts(plan: dict[str, Any], tasks: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """检查同一 parallel batch 内显式声明的 write/write 冲突。"""
    findings = []
    for batch in plan.get("execution", {}).get("batches", []):
        if batch.get("mode") != "parallel":
            continue
        owners: dict[str, str] = {}
        for tid in batch.get("tasks", []):
            task = tasks.get(tid)
            if not task:
                continue
            for resource in task.get("resources", {}).get("write", []):
                resource = str(resource)
                if resource in owners and owners[resource] != tid:
                    findings.append(finding("RES001", f"Parallel batch {batch.get('id')} 中 {owners[resource]} 与 {tid} 同时写 {resource}", affected=[owners[resource], tid, resource]))
                owners[resource] = tid
    return findings


def check_governance(plan: dict[str, Any]) -> list[dict[str, Any]]:
    """检查准备放行时是否仍存在活动 Blocker Issue。"""
    if plan.get("plan", {}).get("state") != "EXECUTION_READY":
        return []
    findings = []
    for issue in plan.get("issues", []):
        if issue.get("severity") == "BLOCKER" and issue.get("status") in BLOCKING_ISSUE_STATES:
            iid = str(issue.get("id", "<unknown>"))
            findings.append(finding("GOV001", f"EXECUTION_READY 时仍存在活动 Blocker: {iid}", affected=[iid]))
    return findings


def lint(plan: dict[str, Any]) -> list[dict[str, Any]]:
    """运行当前实现的核心确定性规则。"""
    tasks, findings = task_map(plan)
    findings += check_requirements(plan, tasks)
    findings += check_dependencies(tasks)
    findings += check_dataflow(tasks)
    findings += check_evidence(plan)
    findings += check_unknowns(plan)
    findings += check_validation(tasks)
    findings += check_runtime(plan)
    findings += check_resource_conflicts(plan, tasks)
    findings += check_governance(plan)
    return findings


def main() -> int:
    """CLI 入口。"""
    parser = argparse.ArgumentParser(description="Plan Governance deterministic lint")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    args = parser.parse_args()

    plan = load_json(args.plan)
    findings = lint(plan)
    if args.json:
        print(json.dumps({"findings": findings}, ensure_ascii=False, indent=2))
    else:
        if not findings:
            print("PASS: 未发现已实现的确定性规则问题")
        for item in findings:
            print(f"[{item['severity']}] {item['rule']}: {item['message']}")
    return 1 if any(x["severity"] == "BLOCKER" for x in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
