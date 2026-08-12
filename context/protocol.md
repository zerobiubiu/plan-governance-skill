# Context Capsule Protocol

## 定义

Context Capsule 不是聊天记录摘要，而是针对某个 Task 从正式治理状态**编译出的最小充分上下文**。

## 三层信息

- MUST_INCLUDE：目标、硬约束、关键输入、前置条件、关键 Fact/Unknown、完成条件、返回契约；
- REFERENCE_ON_DEMAND：大文件、长日志、完整配置、依赖树等只给引用与相关性说明；
- DENY/ISOLATE：Blind Review 时隔离 Planner reasoning、confidence、其他 Validator findings、rejected alternatives 等。

## Capsule 类型

- minimal；
- standard；
- investigation；
- implementation；
- blind-review；
- simulation；
- nested；
- delta。

## Context Expansion

子代理缺信息时顺序：

1. Capsule；
2. upstream output；
3. direct references；
4. 允许 Scope 内局部搜索；
5. 仍无法解决 → structured escalation。

不得默认扫描整个仓库。

## Nested Capsule

二级 Agent 只拿父任务中与子闭环直接相关的子集。Scope/Authority 单调缩小，但允许在授权范围内读取必要的新局部信息。

## Freshness

Capsule 与 task semantic、policy、关键 upstream output、baseline relevance 绑定。关键语义变化后 `STALE` 并重新编译；纯格式变化不失效。

## Budget

使用 compact / standard / expanded 等级，不做伪精确 token 分数。超预算时优先把正文转引用、去重、裁剪背景；不得盲目截尾。若 expanded 仍过大，返回 Task Boundary Diagnostic，而不是无限塞上下文。

## Sufficiency Gate

下放前检查：仅凭 Capsule + 允许读取资源，Agent 能否闭环完成任务？不能则补 Capsule、授权受控检索、生成 Investigation Task，或阻塞。
