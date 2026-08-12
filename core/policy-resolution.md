# Policy Resolution

## 策略层

从低到高：

1. Skill Default；
2. Project Policy；
3. Named Profile；
4. Runtime/Task Profile；
5. 本次用户明确约束；
6. Safety Invariants（最高且不可覆盖）。

## 类型

- `constraint`：硬约束；
- `preference`：软偏好；
- `heuristic`：默认判断规则；
- `review_focus`：本轮审查重点；
- `stage_hook`：阶段 Prompt 插入；
- `task_override`：局部覆盖；
- `optimization_objective`：合法方案之间的优先级。

## 自然语言策略

自然语言 Prompt 先经 Policy Compiler 归类为上述对象，并保留 `original_statement` 以便追踪。不能确定硬/软性质时，保持显式不确定，不擅自升级为硬约束。

## 冲突

- 可由优先级裁决：自动 resolve，并写入 resolution log；
- 同级 hard constraint 冲突：`POLICY_BLOCKED`；
- Profile 不能覆盖 Safety Invariant。

## Capability Negotiation

最终策略必须与 Runtime 能力协商。Profile 希望 8 并发而 Runtime 最多 3 时，应安全降级为分批/串行，而不是产生不可执行 Plan。
