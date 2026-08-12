# Repair Workflow

1. 从 Issue Registry 选择 CONFIRMED / REOPENED 问题；
2. Reconciler 生成 Revision Directive + Revision Envelope；
3. Planner/Scheduler 只在允许 Scope 内修订；
4. 生成 Change Set；
5. Issue → FIXED_UNVERIFIED；
6. 做 Targeted Reverification + Impact-Scoped Regression；
7. 通过后 VERIFIED/CLOSED；失败则 REOPEN/INVESTIGATE/REPLAN。
