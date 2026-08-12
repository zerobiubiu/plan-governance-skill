# Verify Workflow

按三层路由：

1. Deterministic Lint；
2. 针对命中域运行 Semantic Validator；
3. 只有高影响、证据争议、关键 Fact/Assumption 才启动 Independent Evidence Validator。

Independent Validator 默认使用 Blind Review Capsule，多个 Validator 即使串行也不共享彼此 Findings。
