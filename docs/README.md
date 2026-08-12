# Plan Governance Skill 文档索引

## 文档清单

| 文档 | 类型 | 状态 | 说明 |
|---|---|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | 🧭 架构决策 | ✅ 已执行 | 总体架构与权威/派生数据划分 |
| [CUSTOMIZATION.md](CUSTOMIZATION.md) | 🔧 开发指导 | ✅ 已执行 | 自定义接口、Profile 叠加、Task Override |
| [ROLE-PROTOCOLS.md](ROLE-PROTOCOLS.md) | 📄 参考说明 | ✅ 已执行 | 角色职责、可修改范围与禁止事项 |
| [CONVERGENCE-CHECKPOINT.md](CONVERGENCE-CHECKPOINT.md) | 📄 参考说明 | ✅ 已执行 | v0.1 设计冻结检查点 |
| [ISSUE-MATRIX.md](ISSUE-MATRIX.md) | 📄 参考说明 | ✅ 已执行 | Issue 生命周期状态矩阵（根目录为镜像副本） |
| [history.md](history.md) | 🧾 变更记录 | ✅ 已执行 | 增量变更记录（追加型历史文档，只追加不重写） |

## 图例

- **类型**：📋 接口契约 ｜ 🔧 开发指导 ｜ 📄 参考说明 ｜ 🚀 部署运维 ｜ 🧭 架构决策 ｜ 🧾 变更记录
- **状态**：✅ 已执行 ｜ 🔧 待执行 ｜ 📄 参考 ｜ ⚠️ 已过期 ｜ 🚫 已废弃

## 推荐阅读顺序

1. `ARCHITECTURE.md` — 先建立整体架构认知；
2. `ROLE-PROTOCOLS.md` — 理解角色分工与权限边界；
3. `CUSTOMIZATION.md` — 学习如何定制规划策略；
4. `CONVERGENCE-CHECKPOINT.md` — 了解设计冻结范围与扩展原则。

## 相关文件

- 主文档：`../SKILL.md`
- 核心治理：`../core/`（不变量、收敛、调度、风险、模拟等）
- 规则库：`../rules/core-rules.json` 与 `../rules/README.md`
- 工作流：`../workflows/`
- 模板：`../templates/`
- 脚本：`../scripts/`（`self_check.py` 为自检入口）
