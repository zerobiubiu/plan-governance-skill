# Execution Scheduler 与 Bounded Scheduling

## 职责边界

Planner 决定“做什么”；Scheduler 决定“谁来做、何时做、如何传上下文”。Scheduler 不得偷偷创建新的业务语义任务；发现 Semantic Plan 不可调度时返回阻塞/修订请求。

## 四图模型

1. Dependency Graph：正确性和顺序；
2. Dataflow Graph：上游 Output 如何成为下游 Input；
3. Context Affinity Graph：哪些任务共享高成本上下文；
4. Resource Conflict Graph：哪些任务即使无依赖也不能安全并发。

## 决策顺序

1. 建立 hard dependency；
2. 验证 Dataflow；
3. 应用资源排斥；
4. 应用独立性约束；
5. 计算上下文亲和；
6. 识别 critical path；
7. 评估委托收益与成本；
8. 分组并指派逻辑 owner；
9. 生成逻辑并行组；
10. 与 Runtime 能力协商；
11. 输出实际 batch/serial/parallel topology。

## 委托判断

收益：Context isolation、specialization、parallel gain、parent relief。
成本：handoff、context reconstruction、duplicate reads、coordination、API reliability。

不要用伪精确权重；使用 low/medium/high + 可解释理由。

## Bounded Scheduling

### Preferred Topology

Scheduler 给出首选 owner / batch / serial-parallel 方案。

### Allowed Deviations

可声明：

- main agent takeover；
- reuse existing agent；
- parallel → serial；
- batch 重组；
- 等价执行细节变化。

### Protected Boundaries

不得突破：

- hard dependency；
- required independence；
- resource exclusion；
- runtime limits；
- safety constraints；
- forbidden scope。

### 偏离等级

- L0 Free Adaptation：不改变执行语义；
- L1 Bounded Reschedule：只改 Execution IR，需要轻量 execution impact check；
- L2 Governance Change：突破已审边界，必须 STOP → impact analysis → revalidation/replan。

Actual Execution Topology 应记录与 Planned Topology 的差异，用于 Drift 检测和未来调优，但不得自动学习修改规则。
