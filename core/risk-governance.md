# 风险分类与治理等级

## Risk Vector

不使用可被平均掩盖的单一总分。至少建模：

- Impact：I0-I5；
- Reversibility：R0-R4；
- Uncertainty：U0-U4；
- Blast Radius：B0-B4；
- Dependency Complexity：D0-D4；
- Security Sensitivity：S0-S4；
- Verification Difficulty：V0-V4。

## Governance Level

- G0：轻量。Requirement + 简单 Plan + 基础 Lint；
- G1：普通。增加 dependency/dataflow/basic proof；
- G2：复杂。增加 Semantic Validator、Issue tracking、S0 Simulation；
- G3：高风险。增加独立 Validator、Evidence challenge、S1 Simulation、Failure/Rollback Review；
- G4：关键。增加严格独立审查、S2 dry run（若安全）、恢复性模拟和更严格 Gate。

## 安全下限

示例：

- Security >= S3 → 至少 G3；
- Reversibility >= R3 → 至少 G3；
- Uncertainty >= U3 → 必须先 Investigation；
- Production destructive change → 必须 rollback/recovery review；
- Required independent review 不得因低 budget 取消。

Governance Budget 可减少优化性检查，但不能突破 Safety Floor。
