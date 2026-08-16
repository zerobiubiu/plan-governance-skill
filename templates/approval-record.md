# Approval Record（审批记录）

## 查验摘要

- 查验时间 / Inspector（角色）:
- 输入基线: Plan 版本 / Policy 版本 / Issues / Validation / Simulation

## 查验核验项

| 维度 | 结论 | 关键 Finding |
|---|---|---|
| 完整（需求 → 任务 → 验收） | 通过 / 不通过 | |
| 一致（两层 IR / 引用 / 依赖图） | | |
| 证据（Fact / Assumption / Unknown） | | |
| 约束（Hard / 禁止范围 / Policy） | | |
| 状态（Issue disposition） | | |
| 运行（Agent / 并发 / 资源 / Simulation） | | |
| 风险（向量 / 治理等级 / 回滚） | | |

## 决策

- Verdict: APPROVE / APPROVE_WITH_CONDITIONS / REVISE / BLOCK
- Hard Gate: 通过 / 未通过（列出 Blocking Issue）

## 绑定

- Fingerprint（Semantic + Execution + Policy + Baseline）:
- Approver（≠ Plan Author）:
- 有效期 / 复审要求:

## 条件（仅 APPROVE_WITH_CONDITIONS）

| 条件 ID | 内容 | 验收方式 | 关闭时限 | 状态 |
|---|---|---|---|---|

## 声明

- APPROVED ≠ Execution Authorization；执行授权由更高权限 Actor 另行签发。
- 关键变化（Semantic / Execution / Policy / Baseline）使本 Record 自动失效，必须重新查验审批。
