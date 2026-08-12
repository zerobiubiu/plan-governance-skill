# Optimize Workflow

已有 Plan 调优时先分类变更目标：

- Semantic Optimization；
- Execution Optimization；
- Validation Optimization；
- Safety Optimization；
- Presentation Normalization。

默认只修改最小必要层。仅 Agent/并发/上下文策略变化时，保持 Semantic Plan 稳定，重做 Execution Scheduling + Execution Validation。

用户自然语言二次审核 Prompt 作为 Runtime Policy Overlay/Review Focus 注入，而不是改写 Skill 默认规则。
