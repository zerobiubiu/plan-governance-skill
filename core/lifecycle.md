# 生命周期与状态机

## 主状态

```text
INTAKE
  ↓
MODELED
  ↓
DRAFT
  ↓
CANDIDATE
  ↓
INTERNAL_VERIFIED
  ↓
INDEPENDENT_REVIEW
  ↓
AUDIT_READY
  ↓
FINAL_AUDIT
  ↓
EXECUTION_READY
```

## 分支状态

- `REVISION_REQUIRED`：存在确认问题，需要修订；
- `DIRECTION_REJECTED`：原方案方向错误，不能继续修补；
- `BLOCKED_EXTERNAL`：缺少必须的外部输入/证据；
- `POLICY_BLOCKED`：同级硬策略冲突或不可满足；
- `CONVERGENCE_BLOCKED`：循环振荡或无法收敛；
- `STALE`：Plan/Policy/Baseline/关键 Evidence 变化导致批准失效。

## 批准维度

批准至少区分：

- `semantic`；
- `execution`；
- `safety`；
- `evidence`。

仅受影响维度变化时，优先做 Impact-Scoped Revalidation。
