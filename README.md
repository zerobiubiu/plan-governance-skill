# Plan Governance Skill

> 策略驱动的 Plan 编译、验证、调度、第三方审查、模拟与治理 Skill。

将「方案 / 需求 / 已有 Plan」转换为**可执行、可验证、可追踪、可收敛**的执行 Plan，支持通过自然语言、Profile、Runtime 约束与阶段 Hook 自定义规划策略。

本 Skill 不追求「写得最长」，而追求：

- **贴切**：需求可追踪到任务和验收；
- **详细**：关键任务输入、输出、边界、验证清晰；
- **安全**：高风险操作有前置检查、失败路径和回滚；
- **稳定**：调度遵守依赖、资源、Runtime 与上下文约束；
- **可行**：关键事实有证据，关键未知有解决路径；
- **可收敛**：Issue 有生命周期，循环有停止条件；
- **可定制**：默认规则可被项目 / Profile / 本次 Prompt 在安全边界内覆盖。

## 适用场景

- 从方案生成实施 Plan；
- 调优已有 Plan；
- 只验证、只审核或只整理 Plan；
- 迁移、重构、依赖升级、生产变更、数据安全任务；
- 多 Agent / 子代理 / 嵌套 Agent 的执行规划；
- 需要第三方独立校验、执行模拟或高风险审计的 Plan。

## 核心模式

支持：`generate`、`optimize`、`verify`、`audit`、`approve`、`normalize`、`repair`、`simulate`。

```text
用户意图
  ↓
策略解析 / Runtime 能力协商
  ↓
需求建模
  ↓
Semantic Plan 编译
  ↓
确定性 Lint
  ↓
Execution Scheduling
  ↓
内部验证
  ↓
第三方独立验证（按风险启用）
  ↓
Issue 聚合与 Reconcile
  ↓
必要修订 + 定向复验
  ↓
Simulation（按治理等级启用）
  ↓
Final Audit
  ↓
EXECUTION_READY / BLOCKED / DIRECTION_REJECTED
```

## 特性

- **两层 Plan 语义**：Semantic Plan（必须做什么）与 Execution Plan（怎么执行）分离，调整编排时不重写业务语义；
- **不可覆盖的不变量**：Plan Author 不能最终批准自己的 Plan；`APPROVED Plan != Execution Authorization`；未验证假设不得伪装成 Fact（见 `core/invariants.md`）；
- **Bounded Scheduling**：有边界调度，越界变化必须做 Impact Analysis 并按范围重新验证或 Replan；
- **Context Capsule / Authority Envelope**：子代理不继承主会话全文，最小充分上下文 + 授权边界；
- **三层验证**：Deterministic Lint → Semantic Validator → Independent Evidence Validator，按风险启用；
- **Issue 治理**：Finding（不可变观察）与 Issue（聚合裁决后持续追踪）分离，完整生命周期；
- **风险向量与治理等级**：Impact / Reversibility / Uncertainty 等风险维度触发 G0~G4 治理下限，不做平均总分；
- **Simulation**：S0 纯静态 → S1 只读仓库 → S2 Policy 认可的 check/build/test/dry-run，fail-closed；
- **收敛控制**：默认最大修订循环 3 次，blocker 不降或核心假设失效时停止补丁并升级；
- **零第三方依赖**：脚本全部使用 Python 3.11+ 标准库。

## 目录结构

```text
.
├── SKILL.md                  # Skill 主文档（入口）
├── AGENTS.md                 # 本项目开发规范
├── ISSUE-MATRIX.md           # Issue 状态矩阵（镜像 docs/ISSUE-MATRIX.md）
├── core/                     # 核心治理语义（不变量、收敛、调度、风险、模拟等）
├── rules/                    # 确定性规则库（core-rules.json + 编号体系）
├── schemas/                  # JSON Schema（Plan IR、Context Capsule、Finding 等）
├── context/                  # Context Capsule / Return Capsule 协议
├── authority/                # Authority Envelope
├── workflows/                # generate / optimize / verify / audit / approve / repair / simulate
├── templates/                # plan / task / agent-task / audit-report / approval-record / validator-prompt
├── profiles/                 # 规划策略（atoms 原子策略 + presets 预设组合）
├── examples/                 # 示例 Plan
├── scripts/                  # 标准库实现的自检与治理脚本
└── docs/                     # 文档（架构、自定义、角色协议等）
```

## 快速开始

需要 Python 3.11+，推荐使用 [uv](https://docs.astral.sh/uv/)：

```bash
# 运行 Skill 自检（文件完整性 + JSON 有效性 + 示例 Plan lint/gate/simulation）
uv run python scripts/self_check.py

# 对示例 Plan 执行确定性 Lint
uv run python scripts/plan_lint.py examples/sample-plan.json

# 对示例 Plan 执行治理 Gate 检查
uv run python scripts/governance_gate.py examples/sample-plan.json

# 对示例 Plan 执行 S0 静态 Simulation
uv run python scripts/simulate_plan.py examples/sample-plan.json
```

无 uv 时可直接使用 `python`（3.11+）。

## 用法

- **用户给方案** → `workflows/generate.md`
- **用户给已有 Plan 要调优** → `workflows/optimize.md`（先识别是 Semantic / Execution / Validation / Safety / Presentation 优化，避免 Full Replan）
- **用户只要求审核** → `workflows/audit.md`（禁止越权实施）
- **用户要求审批放行 Plan** → `workflows/approve.md`（先查验后审批，审批人不得是 Plan Author，审批绑定 fingerprint）
- **用户给 Audit 结果要求修复** → `workflows/repair.md`（按 Issue / Revision Envelope 定向修复）

### 自定义规划策略

用户可通过自然语言提供 `constraints`、`preferences`、`review_focus`、`custom_rules`、`stage_hooks`、`task_overrides`、`optimization_objective`、`validation_strategy`、`governance_level`、`runtime_profile`。

优先级默认：

```text
Safety Invariants
  > 本次用户硬约束
  > Named Profile / Runtime Override
  > 项目规则
  > Skill 默认规则
```

同级硬约束冲突且无法裁决时进入 `POLICY_BLOCKED`，不得偷偷任选其一。详见 `docs/CUSTOMIZATION.md`。

## 文档

见 `docs/README.md`。

## 许可

[MIT](LICENSE) © 2026 zerobiubiu
