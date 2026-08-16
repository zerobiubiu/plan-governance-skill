---
name: plan-governance-skill
version: 0.1.0
language: zh-CN
description: 策略驱动的 Plan 编译、验证、调度、第三方审查、模拟与治理 Skill。将方案/需求/已有 Plan 转换为可执行、可验证、可追踪、可收敛的执行 Plan，支持自然语言、Profile、Runtime 约束与阶段 Hook 自定义规划策略。
summary: 策略驱动的 Plan 编译、验证、调度、第三方审查、模拟与治理 Skill。
---

# Plan Governance Skill

## 目标

把“方案/需求/已有 Plan”转换为**可执行、可验证、可追踪、可收敛**的执行 Plan，同时允许用户通过自然语言、Profile、Runtime 约束和阶段 Hook 自定义规划策略。

本 Skill 不追求“写得最长”，而追求：

- 贴切：需求可追踪到任务和验收；
- 详细：关键任务输入、输出、边界、验证清晰；
- 安全：高风险操作有前置检查、失败路径和回滚；
- 稳定：调度遵守依赖、资源、Runtime 与上下文约束；
- 可行：关键事实有证据，关键未知有解决路径；
- 可收敛：Issue 有生命周期，循环有停止条件；
- 可定制：默认规则可被项目/Profile/本次 Prompt 在安全边界内覆盖。

## 适用场景

- 从方案生成实施 Plan；
- 调优已有 Plan；
- 只验证、只审核或只整理 Plan；
- 迁移、重构、依赖升级、生产变更、数据安全任务；
- 多 Agent / 子代理 / 嵌套 Agent 的执行规划；
- 需要第三方独立校验、执行模拟或高风险审计的 Plan。

## 核心模式

支持：`generate`、`optimize`、`verify`、`audit`、`approve`、`normalize`、`repair`、`simulate`。

默认遵循：

```text
用户意图
  ↓
策略解析 / Runtime 能力协商
  ↓
需求建模
  ↓
Semantic Plan 编译
  ↓
确定性 Lint
  ↓
Execution Scheduling
  ↓
内部验证
  ↓
第三方独立验证（按风险启用）
  ↓
Issue 聚合与 Reconcile
  ↓
必要修订 + 定向复验
  ↓
Simulation（按治理等级启用）
  ↓
Final Audit
  ↓
EXECUTION_READY / BLOCKED / DIRECTION_REJECTED
```

## 不可覆盖的不变量

必须遵守 `core/invariants.md`。重点：

1. Plan Author 不能最终批准自己的 Plan。
2. 独立 Validator 默认不得继承 Planner 推理历史或其他 Validator Findings。
3. Validator / Simulator 默认只读 Plan，不直接修 Plan。
4. Reconciler 决定如何处理问题；Planner/Scheduler 执行修订；Validator 复验。
5. 未验证关键假设不得伪装成 Fact。
6. Issue 不得静默消失；`FIXED != VERIFIED`。
7. Runtime 不支持的执行拓扑不能进入 `EXECUTION_READY`。
8. `APPROVED Plan != Execution Authorization`。
9. Score 只诊断，Hard Gate 决定放行。
10. Governance 强度必须与风险、复杂度和不确定性成比例。

## Plan 的两层语义

### Semantic Plan

回答“必须做什么”：需求、任务、依赖、输入输出、风险、验证、回滚。

### Execution Plan

回答“怎么执行”：Agent owner、批次、串并行、Context Capsule、Handoff、Bounded Scheduling。

只调整 Agent/并发/上下文时，优先只修改 Execution IR，不重写 Semantic Plan。

## Bounded Scheduling

默认使用有边界调度：

- Scheduler 给出首选执行拓扑；
- 执行者可在 `Allowed Deviations` 内接管、复用 Agent、串行化等；
- 不得突破 hard dependency、独立性、资源冲突、Runtime、安全、禁止范围；
- 越界变化必须做 Impact Analysis，并按范围重新验证或 Replan。

详见 `core/scheduling.md`。

## 子代理原则

只在净收益为正时使用子代理，优先用于：

- 大量中间信息但上级只需要明确结果；
- 边界清晰、输入输出可控的独立闭环；
- 需要第三方独立性；
- 能显著降低上级上下文负担。

不要为了“展示 Agent 能力”拆分。嵌套 Agent 的 Scope 与 Authority 必须相对父级单调缩小。

## Context Capsule

子代理不得默认继承主会话全文。由 Capsule Compiler 为具体 Task 编译最小充分上下文：

- MUST_INCLUDE；
- REFERENCE_ON_DEMAND；
- DENY/ISOLATE。

`Context Capsule` 回答“需要知道什么”；`Authority Envelope` 回答“允许做什么”。

详见 `context/protocol.md` 与 `authority/envelope.md`。

## 验证三层

遵循：

> Deterministic when possible; Semantic when necessary; Independent when consequential.

1. Deterministic Lint：Schema、引用、图、Runtime、Policy、Issue 状态等可确定问题；
2. Semantic Validator：依赖语义、任务边界、验证充分性、Agent 是否值得等；
3. Independent Evidence Validator：关键事实、高风险假设、争议结论的独立重新取证。

规则编号见 `rules/core-rules.json`。

## Issue 治理

Finding 与 Issue 分离：

- Finding：一次检查的不可变观察；
- Issue：多个 Finding 聚合、裁决后持续追踪的治理对象。

生命周期：

```text
OPEN → TRIAGED → CONFIRMED / REJECTED / INVESTIGATE / DEFERRED
CONFIRMED → FIX_PLANNED → FIXED_UNVERIFIED → REVERIFYING → VERIFIED → CLOSED
CLOSED → REOPENED
```

Reconciler 不按多数投票；证据、硬约束、正确性优先于意见数量。

详见 `core/issue-governance.md`。

## 风险与治理等级

使用风险向量，不做平均总分：Impact、Reversibility、Uncertainty、Blast Radius、Dependency Complexity、Security、Verification Difficulty。

Governance Level：`G0`~`G4`。高风险维度触发治理下限，不能被其他低风险维度平均掉。

详见 `core/risk-governance.md`。

## Simulation

Simulation 验证的是**Plan-level executability**，不是实际实现正确性。

层级：

- S0：纯 Plan 静态模拟；
- S1：允许只读仓库；
- S2：允许 Policy 认可的 check/build/test/dry-run。

模拟遵循 fail-closed：关键输入、路径、决策或前置条件缺失时停止，不自行猜测。

详见 `core/simulation.md`。

## 收敛与停止

默认最大修订循环为 3。出现以下情况之一，应停止无意义补丁并升级：

- blocker 两轮不下降；
- 同一 Issue 多次 REOPEN；
- 核心假设失效；
- Semantic churn 过大；
- 新增 blocker 数持续不降；
- 只剩不阻塞的 MINOR/INFO 优化。

最终状态：`EXECUTION_READY`、`BLOCKED_EXTERNAL`、`POLICY_BLOCKED`、`DIRECTION_REJECTED`、`CONVERGENCE_BLOCKED`。

详见 `core/convergence.md`。

## 自定义接口

用户可以自然语言提供：

- `constraints`：硬约束；
- `preferences`：软偏好；
- `review_focus`：本轮重点；
- `custom_rules`：自定义审查规则；
- `stage_hooks`：阶段前后 Prompt；
- `task_overrides`：任务局部覆盖；
- `optimization_objective`：合法方案之间的选择优先级；
- `validation_strategy`；
- `governance_level`；
- `runtime_profile`。

优先级默认：

```text
Safety Invariants
  > 本次用户硬约束
  > Named Profile / Runtime Override
  > 项目规则
  > Skill 默认规则
```

同级硬约束冲突且无法裁决时，进入 `POLICY_BLOCKED`，不得偷偷任选其一。

## 推荐入口流程

### 用户给方案

使用 `workflows/generate.md`。

### 用户给已有 Plan，要调优

使用 `workflows/optimize.md`。先识别是 Semantic、Execution、Validation、Safety 还是 Presentation 优化，避免 Full Replan。

### 用户只要求审核

使用 `workflows/audit.md`，禁止越权实施。

### 用户要求对 Plan 做审批放行

使用 `workflows/approve.md`（先查验、后审批；审批人不得是 Plan Author，审批绑定 fingerprint）。

### 用户给 Audit 结果要求修复

使用 `workflows/repair.md`，按 Issue/Revision Envelope 定向修复。

## 工具脚本

标准库实现，无第三方 Python 依赖：

- `scripts/plan_lint.py`：核心确定性 Lint；
- `scripts/dependency_graph.py`：依赖图与拓扑检查；
- `scripts/policy_merge.py`：策略层合并与冲突记录；
- `scripts/simulate_plan.py`：基础 S0 静态 Simulation；
- `scripts/self_check.py`：Skill 自检。

优先用 `uv run python ...`，无 uv 时可回退到 Python 3.11+。

## 最终输出原则

最终 `plan.md` 面向执行者，应清晰而不过载；治理细节放在独立状态/报告中。执行 Plan 至少说明：目标、前置条件、输入、修改范围、禁止范围、步骤、输出、验证、失败处理、回滚、依赖、Agent 策略和完成条件。
