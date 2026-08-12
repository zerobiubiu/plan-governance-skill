# Issue Registry 与 Reconciler

## Finding 与 Issue

- Finding：某次 Lint/Validator/Simulator 的不可变观察；
- Issue：多个 Finding 经聚合和裁决后形成的持续治理对象。

多个检查路径发现同一根因时，应聚合到一个 Issue，而不是重复创建。

## Issue 生命周期

```text
OPEN → TRIAGED
TRIAGED → REJECTED | INVESTIGATE | DEFERRED | CONFIRMED
CONFIRMED → FIX_PLANNED → FIXED_UNVERIFIED → REVERIFYING → VERIFIED → CLOSED
CLOSED → REOPENED
```

允许 `SUPERSEDED`，但必须指向替代 Issue。

## Root Cause First

Reconciler 优先聚合症状、定位根因，再产生 Revision Directive。禁止每个 Finding 单独打一层补丁。

## 冲突裁决顺序

1. Safety Invariants / Hard Constraints；
2. Verified Evidence；
3. Semantic Correctness；
4. Runtime Feasibility；
5. 用户明确 Preference；
6. Optimization Heuristic。

不按多数投票。多个独立 Finding 一致只提升置信度，不能替代证据。

## Reconciler 输出

Reconciler 不直接改 Plan，而输出：

- disposition；
- root cause；
- remediation owner；
- PATCH / PARTIAL_REPLAN / FULL_REPLAN；
- Revision Directive；
- Revision Envelope；
- required revalidation domains。

## 修复验证

Planner/Scheduler 修改后，Issue 只能到 `FIXED_UNVERIFIED`。必须由规则/Validator/Simulator 证明 Resolution Proof，才能 `VERIFIED`。

## 反振荡

同一 Issue 多次 REOPEN、两轮 blocker 不下降或同类根因反复出现时，停止普通 PATCH，进入 Root Cause Review / Partial Replan。

## 风险接受与 Waiver

- Accepted Risk：问题真实但有权限 Actor 明确接受后果；
- Waiver：某条可豁免治理规则在限定 Scope 内获准不适用。

Safety Invariant 和 hard user constraint 不允许普通 Waiver。Reconciler 只能建议风险接受，不能自行替用户接受重大风险。
