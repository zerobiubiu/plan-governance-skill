# 自定义接口

## 自然语言覆盖

用户可以直接写：

> 当前 API 限速，不要并行执行子代理；最多 3 个 Agent 并发；OMP 允许主→子→二级子，但仅在下一级形成独立闭环且明显降低上层上下文时使用。重点优化依赖、执行顺序、上下文复用和 Agent 切换。

Policy Compiler 应拆为：

- hard constraints：并发上限、嵌套上限、禁止子代理并行；
- preferences：减少调用、减少切换、提高上下文复用；
- review focus：依赖、执行顺序、Agent 编排、上下文效率；
- custom rules：子代理必须有完整 Prompt Contract。

## Profile 叠加示例

```text
migration
+ large-repo
+ omp-rate-limited
+ assumption-zero
+ verification-heavy
```

Profile 不是互斥选择；最终由 Policy Resolution 和 Runtime Capability Negotiation 生成 Effective Policy。

## Task Override

Task 可以声明局部：

- delegation forbidden/recommended/required；
- independence required；
- allowed deviations；
- local governance escalation。

Task Override 不得削弱 Safety Invariant 或越过 Runtime 能力。
