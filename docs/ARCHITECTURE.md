# 总体架构

```text
Policy & Runtime
      ↓
Requirement Model
      ↓
Semantic Plan IR
      ↓
Deterministic Lint
      ↓
Execution Scheduler
      ↓
Execution IR
      ↓
Context Capsule + Authority Envelope
      ↓
Internal / Independent Validation
      ↓
Finding → Issue Registry → Reconciler
      ↓
Revision Directive / Envelope
      ↓
Targeted Revalidation
      ↓
Simulation
      ↓
Final Audit / Convergence Gate
      ↓
EXECUTION_READY
```

## 权威数据与派生数据

权威：Requirements、Tasks、Policy Snapshot、Facts/Unknowns、Decisions、Evidence refs、Issues。

派生：Dependency/Dataflow/Context/Resource Graph、Critical Path、Agent Topology、Coverage Matrix、Markdown Plan、报告。

不得维护两个互相独立的“真相源”。
