# Audit Workflow

Audit 是只读 Gate：

1. 读取 Candidate Plan、Effective Policy、Active Issues、Validation/Simulation 结果；
2. 检查 Hard Gate；
3. 确认批准绑定的 fingerprint/baseline；
4. 输出：APPROVE / REVISE / BLOCK；
5. Auditor 不直接修 Plan，不自动执行。
