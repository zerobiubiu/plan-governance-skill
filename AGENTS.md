# AGENTS.md

## 项目定位

本目录是一个通用 Plan Governance Skill，用于生成、验证、调度、模拟和审核工程执行 Plan。

## 技术与格式

- 文档：简体中文 Markdown。
- 机器状态：JSON；避免要求第三方 YAML 解析依赖。
- 脚本：Python 3.11+ 标准库，优先通过 `uv run python` 执行。
- 不引入非必要第三方依赖。

## 修改规则

1. 修改核心治理语义时同步更新 `SKILL.md` 和相关 `core/*.md`。
2. 新增确定性规则时同步更新 `rules/core-rules.json` 与 `scripts/plan_lint.py`。
3. 公开函数和复杂逻辑使用简体中文 docstring。
4. Normalizer/自动修复不得改变 Plan 语义。
5. 测试或自检产生的临时文件必须清理。
6. 修改后运行：
   - `uv run python scripts/self_check.py`，或
   - `python scripts/self_check.py`。
