# Rule System

统一编号：

- `SCH`：Schema/结构；
- `REQ`：需求覆盖；
- `DEP`：依赖；
- `DATA`：输入输出/Dataflow；
- `CTX`：上下文；
- `AGT`：Agent；
- `RES`：资源冲突；
- `POL`：Policy/Runtime；
- `EVD`：证据；
- `UNK`：Unknown/Assumption；
- `SAFE`：安全/回滚；
- `VAL`：验证/Proof；
- `GOV`：治理状态；
- `DRF`：Drift/Staleness；
- `SIM`：Simulation。

编号建议：001-099 deterministic；100-199 semantic；200-299 independent evidence。

一个 Finding 只选一个 primary rule，可列 related rules。规则库不限制推理：发现未覆盖问题时可使用 `GEN000`，后续再决定是否升级为正式规则。
