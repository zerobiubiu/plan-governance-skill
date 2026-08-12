# Authority Envelope

Authority Envelope 与 Context Capsule 分离，明确“Agent 有权做什么”。

建议字段：

- task_scope；
- may：read_repository / modify_declared_scope / run_tests / local_reorder / delegate；
- may_not：expand_scope / modify_other_tasks / deploy / destructive_write；
- delegation_depth_remaining；
- scheduling_authority；
- allowed_resource_scope；
- forbidden_resource_scope。

子代理、二级子代理不得继承父级未显式下放的权限。独立 Validator 默认 Plan/project read-only；Simulation 权限见 `core/simulation.md`。
