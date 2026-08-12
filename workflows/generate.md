# Generate Workflow

1. 解析用户真实目标，区分 Requirement / Constraint / Preference / Unknown。
2. 合并 Policy 并做 Runtime Capability Negotiation。
3. 评估 Risk Vector，选择最低充分 Governance Level。
4. 建立 Requirement Model、Fact/Assumption/Unknown。
5. 编译 Semantic Plan IR；不得根据未验证假设展开关键实现。
6. 跑 Deterministic Lint。
7. Scheduler 生成 Execution IR 与 Bounded Scheduling。
8. 按治理等级运行 Semantic/Independent Validator。
9. Finding → Issue → Reconciler → 必要 Revision。
10. 按治理等级运行 Simulation。
11. Final Audit：Hard Gate 通过后标记 `EXECUTION_READY`，但不得自动执行。
12. 渲染面向人的 `plan.md`，治理元信息保持独立。
