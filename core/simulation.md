# Simulation Engine

## 定位

Simulation 证明的是 **Plan-level executability**，不是实际实现 correctness。

- Lint：结构是否合法；
- Validator：语义是否合理；
- Simulation：严格按 Plan 是否能走通；
- Real Test/Execution：实现是否真实工作。

## 层级

- S0 Static：只读 Plan/Policy/Runtime/Capsule；
- S1 Repository-Assisted：允许只读仓库；
- S2 Tool-Assisted Dry Run：允许 Policy 明确认可的 check/build/test/dry-run，但默认禁止真实部署和破坏性写入。

## Task 模拟九步

1. Eligibility；
2. Preconditions；
3. Input Resolution；
4. Context Resolution；
5. Authority Check；
6. Action Feasibility；
7. Output Projection；
8. Validation / Proof；
9. Transition。

关键缺失采用 fail-closed，不自行猜测。

## 输出状态

模拟产物必须标 `PROJECTED`，不得伪装成真实 `MATERIALIZED/VERIFIED`。

## 路径

按风险选择：

- Happy path；
- Critical failure injection；
- Rollback path；
- Decision branches；
- Agent handoff；
- Bounded scheduling deviation；
- G4 可增加 recoverability/runtime degradation。

禁止穷举全部组合导致状态爆炸。

## Unknown 与 Symbolic Value

有明确 resolution contract 的执行期未知可用 symbolic value 继续；无解决路径的关键未知必须 BLOCK。

## Trace

输出结构化 Execution Trace + Findings + Coverage。Simulator 不直接改 Plan；Finding 进入 Issue Registry。
