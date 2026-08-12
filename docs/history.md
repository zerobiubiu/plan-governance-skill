# 变更记录

## 2026-08-12 — 开源化 plan-governance-skill 并推送 GitHub

- **需求摘要**：将当前 Skill 创建为开源项目，补齐缺失内容，使用 MIT 协议，通过 gh 推送到 GitHub（zerobiubiu）。
- **执行结果**：补齐根 README.md、LICENSE（MIT）、pyproject.toml、.gitignore、docs/README.md 文档索引；`git init` 初始化仓库并完成首次提交；`gh repo create` 创建公开仓库并推送 `main` 分支。
- **影响范围**：项目根目录新增开源脚手架与文档文件；核心治理语义（core/、rules/、scripts/）未改动。
- **验证情况**：`uv run python scripts/self_check.py` 通过（SELF CHECK PASSED）；`gh repo view` 确认仓库为 PUBLIC、默认分支 main、许可证识别为 MIT License。
- **关联文档**：`README.md`、`LICENSE`、`docs/README.md`。


## 2026-08-12 — 移除 pyproject.toml 与 uv.lock（修复 Prime Agent 技能加载警告）

- **需求摘要**：Prime Agent 技能加载器将任何含 `pyproject.toml` 的技能目录判定为 Python 技能候选，并要求存在 `src/<导入名>/__init__.py`，缺失时每次会话输出警告；本技能为 Markdown 工作流技能 + CLI 脚本，`pyproject.toml` 仅含元数据（零依赖、无 build-system、无 tool 配置），无实际功能载荷。
- **执行结果**：删除根目录 `pyproject.toml` 与 `uv.lock`；脚本运行方式不变（`uv run python scripts/*.py` 在无项目根时回退默认环境，仍可用）。
- **影响范围**：项目根目录移除两个无效文件；核心治理语义（core/、rules/、scripts/）未改动。技能在 Prime Agent 中保持 Markdown 分类，加载警告消除。
- **验证情况**：`python scripts/self_check.py` 与 `uv run python scripts/self_check.py` 均通过（SELF CHECK PASSED，rc=0）。
- **关联文档**：`docs/history.md` 2026-08-12 开源化条目（其中提及的 pyproject.toml 现已移除，属历史事实，不重写）。
