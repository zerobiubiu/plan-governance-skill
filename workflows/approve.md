# Approve & Inspect Workflow（审批查验模式）

审批查验是「先查验、后审批」的两段式只读 Gate：

- 与 `audit` 的区别：查验产出**证据核验记录**，审批产出**绑定 fingerprint 的决策**；
- 与 `verify` 的区别：审批是面向放行的决策动作，不是验证过程本身。

## 阶段一：查验（Inspection）

1. 输入采集：Candidate Plan（Semantic + Execution IR）、Effective Policy、需求模型、Active Issues、Validation/Simulation 结果；
2. 按查验清单逐项核对（只产出 Finding，不修改 Plan）：
   - **完整**：Mandatory Requirement → Task → 验收 全覆盖（REQ001 / REQ101）；
   - **一致**：两层 IR 一致，引用与依赖图闭合（SCH002 / DEP001 / DEP002）；
   - **证据**：Verified Fact 有 Evidence，Assumption/Unknown 有验证路径（EVD001 / EVD101 / UNK001 / UNK002）；
   - **约束**：Hard Constraint、禁止范围、Policy 冲突已裁决（POL001 / POL003）；
   - **状态**：Issue 均有 disposition，FIXED_UNVERIFIED ≠ VERIFIED（GOV001 / GOV002）；
   - **运行**：Agent 拓扑、并发、资源、Simulation 约束满足（AGT* / RES* / SIM*）；
   - **风险**：风险向量与治理等级匹配，高影响项有完成条件、失败处理、回滚（SAFE002 / SAFE101 / VAL001）；
3. 产出 Inspection Report：逐项结论 + Findings 列表（按规则编号）。

## 阶段二：审批（Approval）

4. Reconciler 聚合 Findings → Issue 裁决，确认 Hard Gate 状态；
5. 审批人（Invariant 1：不得是 Plan Author）决策：

   | Verdict | 条件 |
   |---|---|
   | APPROVE | Hard Gate 全过、无未处理 Blocker |
   | APPROVE_WITH_CONDITIONS | 仅剩非阻塞条件，且条件可验证、有验收方式、有关闭时限（APV101） |
   | REVISE / BLOCK | 存在 Blocker 或方向问题，不签发审批 |

6. 生成 Approval Record：fingerprint 绑定、决策、条件清单、审批人、有效期、复审要求（模板见 `templates/approval-record.md`）；
7. 条件关闭 → 定向复验 → 更新 Record；关键变化（Semantic / Execution / Policy / Baseline）使审批自动失效（Invariant 9 / GOV005），失效后重新走查验。

## 不变量

- Plan Author 不得审批自己的 Plan（Invariant 1 / APV001）；
- 审批必须绑定 fingerprint，失配即失效（Invariant 9 / APV002）；
- 条件未满足的审批不得当作无条件批准（APV003）；
- APPROVED ≠ Execution Authorization（Invariant 10）；
- Gate 高于 Score（Invariant 15）。

## 角色

| 角色 | 核心职责 | 可修改 | 禁止 |
|---|---|---|---|
| Inspector | 逐项查验、产出 Finding | Inspection Report / Finding | 修 Plan |
| Reconciler | 裁决 Issue、确认 Gate 状态 | Issue / Verdict | 修 Plan |
| Approver | 签发 Approval Record | Approval Record | 审批自己的 Plan |
