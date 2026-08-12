# Convergence Engine

## 目标

避免 Plan 循环变成“越审越长、永远不结束”。

## 默认循环预算

默认最多 3 个完整修订循环。Profile 可调整，但不得无限循环。

## 放行前提

至少满足：

- hard policy conflict = 0；
- unresolved blocking issue = 0；
- planning blocker unknown = 0；
- mandatory requirement uncovered = 0；
- required validation/simulation 已完成；
- runtime topology 合规；
- required proof path 存在；
- required independent validation 已通过。

## 提前收敛

若 Hard Gate 全部通过，且新一轮只剩不阻塞的 MINOR/INFO 优化，不再为了“更漂亮”继续循环。

## 振荡/停机条件

出现任一情况时停止普通 patch：

- blocker 两轮不下降；
- 同一 Issue REOPEN >= 2；
- 同一 Task 关键属性反复翻转；
- 核心假设失效；
- Semantic Plan 大面积替换；
- 每轮修复持续引入同等级新 blocker；
- 外部事实无法获取。

处理：Root Cause Review → PARTIAL/FULL REPLAN；仍无法解决则 `CONVERGENCE_BLOCKED` 或 `BLOCKED_EXTERNAL`。

## Replan 触发

优先 Full/Partial Replan，而不是继续 patch：

- 架构方向变化；
- 核心事实/假设被推翻；
- 关键 Dependency/Dataflow 大面积变化；
- 多个 downstream Task 同时失效。
