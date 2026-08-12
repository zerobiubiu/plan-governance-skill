# Return Capsule

子代理默认不回传完整思考/日志，而回传结构化结果：

- status；
- conclusions；
- outputs；
- evidence refs；
- changed files（若有修改权限）；
- tests/checks；
- unknowns；
- findings/risks；
- scheduling deviations；
- follow-up needs。

Return Capsule 中 Output 应可直接进入 Plan Dataflow；Evidence/Unknown/Finding 可进入对应治理账本。跨 Scope 问题只作为 Finding 回传，不允许子代理自行扩大修改范围。
