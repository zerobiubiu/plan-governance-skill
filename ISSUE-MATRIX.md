# 总设计问题与最终处理矩阵

本文件用于说明本 Skill 在设计收敛时集中处理的主要问题。

| # | 问题 | 最终处理 |
|---|---|---|
| 1 | Plan 只是 Markdown，难以可靠验证 | 采用 Plan IR 作为权威源，Markdown 仅展示 |
| 2 | 业务任务与 Agent 调度耦合 | 分离 Semantic IR 与 Execution IR |
| 3 | 自定义 Prompt 容易被默认规则吞掉 | 建立 Policy Overlay、Profile、Task Override、Stage Hook |
| 4 | Profile 太多导致维护爆炸 | Atomic Policy + Preset Profile 组合 |
| 5 | Runtime 能力与 Plan 不匹配 | Capability Negotiator + 安全降级 |
| 6 | Planner 自审产生确认偏差 | Independent Validation Gate + Blind Review |
| 7 | 多 Validator 相互锚定 | Context Firewall；串行也不共享 Findings |
| 8 | 子代理上下文污染/重复读取 | Context Capsule + Return Capsule + Delta Capsule |
| 9 | 子代理权限膨胀 | Authority Envelope；嵌套 Scope/Authority 单调缩小 |
| 10 | Agent 被机械拆分 | Delegation Benefit/Cost + Context Affinity |
| 11 | 能并行不代表值得并行 | 四图模型 + critical path + resource/failure coupling |
| 12 | 调度太死或太松 | Bounded Scheduling + Protected Boundaries |
| 13 | 执行现场偏离 Plan | Deviation level + Actual Topology + Drift 检查 |
| 14 | Fact/Assumption/Unknown 混淆 | 正式分类 + Evidence Ledger + forbidden assumptions |
| 15 | 关键 Unknown 阻塞或被乱猜 | planning_blocker / execution_resolvable / noncritical |
| 16 | 所有检查都交 LLM 成本高 | Deterministic / Semantic / Independent 三层验证 |
| 17 | 脚本越权判断语义 | Lint 仅检查可确定事实；语义交 Validator |
| 18 | Reviewer 为凑问题制造噪音 | 反迎合协议：无证据可标 UNVERIFIED，不强行找问题 |
| 19 | Findings 重复导致 Issue 爆炸 | Finding/Issue 分离 + root-cause clustering |
| 20 | Issue 在新版中静默消失 | Issue 生命周期 + GOV002 |
| 21 | 作者声称修复即关闭 | FIXED_UNVERIFIED → 独立复验 → VERIFIED |
| 22 | 多 Reviewer 意见冲突 | Reconciler 按 Evidence/Policy/Correctness 裁决，不投票 |
| 23 | 修一个问题破坏其他部分 | Targeted Reverify + Impact-Scoped Regression |
| 24 | 一直 patch 不收敛 | Reopen/Blocker/Churn 检测 + Partial/Full Replan |
| 25 | 评分掩盖致命问题 | Hard Gate 决策，Score 只诊断 |
| 26 | Plan 通过后仓库/策略已变化 | Fingerprint + STALE + Impact-Scoped Revalidation |
| 27 | Plan Approval 被误当执行授权 | EXECUTION_READY 与 Execution Authorization 分离 |
| 28 | 小任务也跑全套治理 | Risk Vector + G0-G4 + Governance Budget |
| 29 | 高风险被平均分稀释 | 风险向量 + Safety Floor，不做单平均总分 |
| 30 | Plan 看起来正确但实际走不通 | S0/S1/S2 Simulation + fail-closed Execution Trace |
| 31 | Simulation 被误当真实测试 | PROJECTED/MATERIALIZED/VERIFIED 状态分离 |
| 32 | 模拟路径爆炸 | Risk-based path selection，不穷举 |
| 33 | Rollback 只是口号 | Restoration Invariants + rollback simulation |
| 34 | 任务完成定义模糊 | Proof Obligation + Requirement→Task→Output→Validation→Proof |
| 35 | 修复 Scope 越来越大 | Revision Directive + Revision Envelope |
| 36 | 治理系统本身越来越臃肿 | Anti-overengineering：默认最低充分机制，只有风险触发升级 |
| 37 | 规则库限制模型发现新问题 | `GEN000` 新问题出口 |
| 38 | 长对话导致设计遗忘 | 关键决策阶段性持久化；最终以本 Skill 文件为冻结规格 |
