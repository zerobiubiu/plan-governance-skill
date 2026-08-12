# Simulate Workflow

1. 选择 S0/S1/S2；
2. 创建 Simulation Capsule 与低权限 Authority Envelope；
3. 建立初始 symbolic state；
4. 先跑 happy path；
5. 按 Risk 选择关键 failure/rollback/branch/handoff/deviation 路径；
6. 输出 Trace + Findings + Coverage；
7. Finding 进入 Issue Registry；
8. 修复后从最近稳定 Checkpoint 做增量重演。
