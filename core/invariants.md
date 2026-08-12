# 宪法级不变量

以下规则不可被普通 Profile、项目规则或 Task override 降级。

1. **作者与最终裁决分离**：Plan Author 不得最终批准自己的 Plan。
2. **独立性优先**：要求 independent validation 时，Validator 不得是作者 Agent。
3. **独立上下文**：Blind Validator 默认不得看到 Planner reasoning、Planner confidence、Decision rationale、其他 Validator findings、rejected alternatives。
4. **审查者只读**：Validator/Simulator 默认不直接改 Plan；发现问题只产生 Finding。
5. **职责分离**：Reconciler 裁决；Planner/Scheduler 修订；Validator 复验。
6. **事实纪律**：关键 Assumption/Unknown 未验证前不得转换成 Fact。
7. **Issue 不可消失**：旧 Issue 必须有 disposition；`FIXED_UNVERIFIED` 不得视为 `VERIFIED/CLOSED`。
8. **Runtime 可执行性**：超出并发、嵌套、工具或权限能力的拓扑不得放行。
9. **批准绑定版本**：Semantic/Execution/Policy/Baseline 关键变化会使相应 Approval 失效。
10. **批准不等于执行授权**：`EXECUTION_READY` 只代表计划质量门槛通过。
11. **高风险必须可证明**：高风险任务必须有明确完成条件、失败处理和必要回滚/恢复说明。
12. **治理成本成比例**：不能对低风险小任务机械启用全套审计。
13. **子代理必须有净收益**：不得为了拆分而拆分。
14. **独立不等于并行**：可以串行调用独立 Validator，但不得共享彼此结论。
15. **Gate 高于 Score**：评分仅诊断，Hard Gate 决定是否可放行。
16. **Context 与 Authority 分离**：知道某信息不代表有权修改其来源。
17. **嵌套权限单调缩小**：子/二级子代理的 Scope 和 Authority 不得超过父级授权。
18. **关键未知 Fail Closed**：关键缺失信息不得用“应该/估计/通常”隐式补全。
