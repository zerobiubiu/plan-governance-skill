# 角色协议

| 角色 | 核心职责 | 可修改 | 禁止 |
|---|---|---|---|
| Policy Compiler | 合并/编译策略 | Policy IR | 改 Plan |
| Requirement Modeler | 建模需求与边界 | Requirement Model | 设计实现任务 |
| Planner | 编译 Semantic Plan | Semantic IR | 自己最终批准 |
| Scheduler | 生成执行拓扑 | Execution IR | 改业务语义 |
| Normalizer | 无语义整理 | Presentation/安全格式修复 | 改依赖/Scope/风险 |
| Internal Verifier | 快速自检 | Finding | 直接修 Plan |
| Independent Validator | 第三方语义/证据校验 | Finding | 看 Planner reasoning、直接改 Plan |
| Simulator | 执行轨迹演练 | Finding/Trace | 真实破坏性执行 |
| Reconciler | 聚合 Issue、裁决、下修订指令 | Issue/Directive | 亲自重写 Plan |
| Auditor | 最终 Gate | Approval/Verdict | 修 Plan 或自动执行 |
