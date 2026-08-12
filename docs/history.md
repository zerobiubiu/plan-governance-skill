# 变更记录

## 2026-08-12 — 开源化 plan-governance-skill 并推送 GitHub

- **需求摘要**：将当前 Skill 创建为开源项目，补齐缺失内容，使用 MIT 协议，通过 gh 推送到 GitHub（zerobiubiu）。
- **执行结果**：补齐根 README.md、LICENSE（MIT）、pyproject.toml、.gitignore、docs/README.md 文档索引；`git init` 初始化仓库并完成首次提交；`gh repo create` 创建公开仓库并推送 `main` 分支。
- **影响范围**：项目根目录新增开源脚手架与文档文件；核心治理语义（core/、rules/、scripts/）未改动。
- **验证情况**：`uv run python scripts/self_check.py` 通过（SELF CHECK PASSED）；`gh repo view` 确认仓库为 PUBLIC、默认分支 main、许可证识别为 MIT License。
- **关联文档**：`README.md`、`LICENSE`、`docs/README.md`。
