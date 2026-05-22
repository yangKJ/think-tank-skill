# think-tank

think-tank 是一个跨平台、可复用的高阶 Skill，用于多角色信息收集、协作分析、讨论审议与结论汇总。

![think-tank hero](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/think-tank-hero-image2.png)

它是本仓库的唯一主品牌、唯一主协议、唯一长期演进对象。research、agent-council、review、strategy 等能力都应收敛为 think-tank 的场景模式或历史实现来源，而不是与 think-tank 平行发展的独立体系。

## 定位

think-tank 不是：

- 某个平台专属脚本壳
- 某个 agent 的附属 prompt
- 某个项目私有实现
- research 的子模块
- agent-council 的改名版本

think-tank 是：

- 一个独立主仓
- 一个统一协议源
- 一个跨平台适配的技能系统
- 一个能被 Claude Code、Codex、其他项目和其他用户复用的能力框架

## 核心能力

一句话理解：

```text
think-tank = 任务理解 + 角色组织 + 能力路由 + 证据汇总 + 边界声明
```

工具型 peer skills 负责搜索、下载、浏览器、知识库、社媒等具体执行；think-tank 只负责任务协议、角色协作、provider 边界和最终结构化结论。

## 典型场景

| Research | Council | Review |
|---|---|---|
| ![research scenario](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/research-card-image2.png) | ![council scenario](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/council-card-image2.png) | ![review scenario](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/review-card-image2.png) |

- 多渠道信息收集
- 多角色分析
- 协作讨论
- 观点碰撞
- 汇总结论
- 输出行动建议

## 公开发布姿态

```yaml
release_posture: stable_release
default_platform: codex
default_runtime: codex_first_runtime_with_verified_partial_subagent_write_lifecycle
supported_for_daily_use:
  - protocol-first research
  - review and strategy workflows
  - local file and user-provided material analysis
not_yet_stable:
  - full cross-platform multi-agent runtime
  - private knowledge-base writes
  - arbitrary external provider invocation without per-provider evidence
```

如果外部用户要直接使用，当前最准确的预期是：

- core protocol 可以用
- Codex 主路径可用
- stable release 只承诺已证据化边界内的能力
- optional capability 需要按 provider 单独验证
- 未验证能力必须保留 `planned`、`blocked` 或 `verified_partial`

## 当前主线补充

think-tank 当前仍然是高阶 Skill core，不再承担 Codex 主 agent 领导者系统的主语。

主 agent 领导者编排主线已迁移到外部 sibling 项目：

```text
Desktop/leader-runtime-project
```

该同级文档定义：

- 主 agent 的领导者身份
- 全量专家池与项目裁剪专家池的关系
- Codex 平台中的派遣、回收、验收和降级边界
- 其他 Codex 项目如何派生自己的领导者主 agent

think-tank 在这里的角色，是被外部 `leader-runtime` sibling 项目编排和调用的高阶技能系统。

## 三层结构

```text
think-tank-skill/
├── SKILL.md
├── README.md
├── protocol/
├── capabilities/
├── profiles/
├── recipes/
├── routing/
├── platforms/
├── modes/
├── runtime/
├── self-tests/
├── templates/
├── domain-packs/
├── docs/
└── examples/
```

### protocol

协议层是 think-tank 的唯一真相源，必须平台无关。它定义输入格式、intent 语义、角色选择、流程阶段、终止条件、输出结构和质量标准。具体触发词不属于 core，应由 routing policy 配置。

### platforms

平台适配层负责把同一套协议落到不同运行环境。Claude Code 和 Codex 可以有不同 runtime、subagent 调用方式、目录结构、记忆落点与 hook 方式，但不能改变 think-tank 的核心行为协议。

### capabilities

能力槽层定义 think-tank 如何与工具型能力共存。具体工具或 skill 名不应被复制进 core，也不应写成通用协议依赖，而应由平台适配层在运行时发现并注册为 capability provider。

### recipes

任务配方层定义跨项目可复用的任务类型，例如竞争分析、市场调研、技术调研、舆情分析、会议审议、验收审查和持续监控。recipe 只声明角色、能力槽和 optional peer skills，不拥有工具。

### routing

技能路由中间层定义 capability 如何连接到当前平台可用的能力提供者。它取代旧任务编排技能那种“任务配方、工具连接、报告输出混在一起”的模式，把连接逻辑拆成 `policy_route`、`skill_route`、`dispatch_decision` 和 `result_recovery`。通用 router 不维护具体 skill 名单，具体名称只能来自平台 adapter、本地 registry、routing policy 或用户显式指定。

### policy

routing policy 定义触发词、intent、recipe、capability 和 provider 偏好。用户可以通过平台示例 YAML 创建项目本地策略，例如 `.think-tank/provider-policy.yaml`。本地 policy 属于项目实例配置，不属于公开 Skill 源。policy 缺失时 think-tank 仍按 core protocol 降级运行。

### local workspace

`.think-tank/` 是项目本地实例工作区，用于放置本项目自己的 provider policy、memory candidates、run logs 和 artifacts。它默认应被 Git 忽略，不能作为公开 Skill 源发布。公开仓库只提供 `templates/`、`schemas/`、`examples/` 和 `protocol/` 中的通用说明。

### skill experience

面向 agent 的 Skill Experience Layer：

- `protocol/skill-trigger-intelligence.md`：判断是否应该使用 think-tank，同时明确触发词由用户 YAML policy 拥有，不是 core 内置规则。
- `protocol/skill-invocation-contract.md`：定义 agent 使用 think-tank 前后的最小契约。
- `protocol/progressive-disclosure.md`：定义渐进加载顺序，避免一次性加载整个仓库。
- `docs/agent-compatibility-matrix.md`：说明 Codex、Claude Code 和通用 agent 的能力差异与降级边界。
- `docs/skill-composition-guide.md`：说明 think-tank 与 optional peer skills 的责任拆分。
- `docs/skill-quality-score.md`：给公开 Skill 可用性和边界清晰度打分。
- `self-tests/`：公开 self-test fixtures，用来检查 trigger、anti-trigger、provider boundary、composition 和 memory write 边界。

### memory curation

项目记忆沉淀把一次讨论、验收或调研中的稳定经验整理成候选记忆，再由用户或项目维护者决定是否下沉到本地 `.think-tank/memory/`、项目规则或公开文档。默认行为是 `propose_then_review`，不自动写入外部知识库。

### capability evidence

能力状态必须按证据链声明：`installed`、`discovered`、`selected`、`dispatched`、`invoked`、`recovered`、`verified_partial` 和 `verified` 不能混用。选中 provider 不等于调用 provider，调用成功也不等于完整 runtime 已验证。

### runtime provenance

所有 think-tank 风格输出必须声明 `runtime_provenance`。如果数据来自助手直接工具调用，要写 `data_collection: direct_assistant_tool`；如果只是单 agent 多 profile，要写 `true_multi_agent_runtime: false`；如果没有真实 provider dispatch，不能声称 provider 已调用或结果已自动回收。

### memory promotion

记忆提升规则决定候选记忆能否从 `.think-tank/memory/` 提升到 `AGENTS.md`、项目文档或公开协议。默认先本地保留，只有平台无关、公开安全、带证据和过期规则的内容才能进入公开 think-tank。

### profiles

角色模板层定义跨平台角色能力。旧 research agent 的 subagents 应被吸收为 profile，而不是原样进入 core。

### modes

场景模式层定义不同使用场景的默认角色、流程强度和输出重点。第一批模式包括：

- `research mode`：承接原 research 体系里的 think-tank 用法
- `council mode`：收编 agent-council 的多角色讨论能力
- `review mode`：用于代码、方案、报告、实现产物审查
- `strategy mode`：用于产品、架构、路线和决策推演

### domain-packs

领域包层承接可选领域知识。当前主仓不内置任何私有领域包；具体项目可以在自己的仓库中添加 domain pack 或本地资料。

## 与历史体系的关系

历史迁移资料只作为维护者背景，不是外部用户第一入口。第一次使用请优先读：

```text
docs/open-source-quickstart.md
docs/support-matrix.md
docs/validation-tiers.md
docs/provider-ecosystem-examples.md
docs/provider-integration-patterns.md
docs/codex-installation.md
docs/first-run-guide.md
docs/operator-manual.md
docs/cookbook.md
docs/progression-guide.md
examples/public/
examples/v3/
../CHANGELOG.md
docs/history.md
```

## 用户操作路径

- `docs/first-run-guide.md`：帮助新用户跑通第一次成功使用。
- `docs/operator-manual.md`：解释 mode、policy、capability、provider boundary 和操作模型。
- `docs/cookbook.md`：给出典型场景做法。
- `docs/progression-guide.md`：说明 beginner、intermediate、advanced 三层上限如何提升。

## Research OS + Memory Runtime

Research OS + Memory Runtime 提供一组平台无关的长期运行契约：

![Research OS and Memory Runtime](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/research-os-memory-runtime-image2.png)

- `protocol/run-record.md`：让一次运行可回放。
- `protocol/project-memory-runtime.md`：把结论沉淀成有来源、有过期规则、有提升决策的 memory candidate。
- `protocol/provider-invocation-ledger.md`：记录 provider 从 selected 到 invoked/recovered/verified 的真实状态。
- `protocol/handoff-protocol.md`：定义 profile、subagent、provider 和 human handoff 的上下文过滤。
- `protocol/guardrails.md`：定义权限、隐私、证据、artifact、memory 和 security gate。
- `protocol/research-os.md`：定义用户本地 `.think-tank/` 工作区结构。
- `protocol/eval-pack.md`：定义协议回归评测样例。

## Open Source Usability

- `templates/research-workspace/`：Research OS starter kit。
- `evals/`：轻量协议回归 fixture。
- `docs/provider-test-matrix.md`：provider pattern 到 provider ledger 的测试矩阵。
- `docs/index.md`：文档站入口，含 concepts、guides、reference 和 release 分区。
- `../CHANGELOG.md`：公开版本演进记录。
- 根目录社区文件：`CONTRIBUTING.md`、`SECURITY.md`、`CODE_OF_CONDUCT.md`、`SUPPORT.md`。

## Skill Experience Layer

Skill Experience Layer 的重点不是增加更重的 runtime，而是让 agent 更容易正确使用这个 Skill：

- 先判断任务是否需要 think-tank。
- 再形成 `think_tank_invocation`。
- 再按 `progressive_disclosure_plan` 加载最小必要文档。
- 需要 optional peer skill 时，先形成 dispatch decision，再区分 selected、invoked、recovered 和 verified。
- 最后用 `self-tests/` 和 `checks/skill_experience_check.py` 检查边界。

触发词、别名和 provider 偏好必须留在用户自己的 YAML policy 中。公开 core 只提供 intent 识别、policy schema、协议契约和样例。

- research 是 think-tank 的一个核心应用场景，主要负责信息收集、证据整理和研究结论输出。
- agent-council 是 think-tank 的历史实现分支或 council mode 来源，主要沉淀多角色讨论、交叉质询和审议机制。
- 旧实现资产应逐步迁入 think-tank 的协议、模式或平台适配目录，不应继续作为新体系中心。

## 第一批建设目标

1. 固化 think-tank 的主仓定位。
2. 建立协议层、平台适配层、模式层的目录边界。
3. 明确 research 与 agent-council 在新体系里的位置。
4. 创建可被 Claude Code 和 Codex 读取的统一 Skill 入口。
5. 为后续吸收旧资产保留清晰迁移路径。

## Codex 验证状态

Codex 当前已完成 foundation 验收：

- `research mode`：verified
- `council mode`：verified
- `review mode`：verified
- `strategy mode`：verified
- capability 降级：verified
- Browser localhost fixture：verified optional
- JSON schema sample：verified

验收命令：

```bash
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/claude_code_validation_check.py
python3 checks/claude_dispatch_sample_check.py
python3 checks/claude_runtime_sample_check.py
python3 checks/minimal_runtime_execution_check.py
python3 checks/capability_queue_check.py
python3 checks/schema_sample_check.py
python3 checks/runtime_contract_check.py
python3 checks/slot_contract_check.py
python3 checks/consensus_contract_check.py
python3 checks/research_protocol_check.py
python3 checks/runtime_planner_check.py
python3 checks/slot_resolver_check.py
python3 checks/state_model_check.py
python3 checks/consensus_runtime_check.py
python3 checks/runtime_result_schema_check.py
python3 checks/codex_runtime_pipeline_check.py
python3 checks/claude_runtime_pipeline_spec_check.py
python3 checks/runtime_e2e_fixture_check.py
python3 checks/runtime_safety_check.py
python3 checks/template_check.py
python3 checks/legacy_think_tank_migration_check.py
python3 checks/research_agent_full_migration_check.py
python3 checks/agent_council_full_migration_check.py
python3 checks/council_runtime_check.py
python3 checks/subagent_runtime_check.py
python3 checks/role_result_schema_check.py
python3 checks/specialist_runtime_contract_check.py
python3 checks/codex_installed_skill_check.py
python3 checks/codex_external_skills_check.py
python3 checks/codex_provider_registry_check.py
python3 checks/codex_provider_policy_check.py
python3 checks/codex_trigger_routing_check.py
python3 checks/codex_runtime_verification_matrix_check.py
python3 checks/routing_layer_check.py
python3 checks/intent_recipe_check.py
python3 checks/local_workspace_check.py
python3 checks/memory_curation_check.py
python3 checks/capability_evidence_state_check.py
python3 checks/memory_promotion_policy_check.py
python3 checks/runtime_provenance_check.py
python3 checks/release_privacy_check.py
```

旧 Claude Code 版 think-tank 已完成迁移处置：

- 可复用 runtime 安全能力进入 `runtime/safety.py`
- 旧输出模板进入 `templates/`
- Claude Code Agent Team 历史运行经验进入 `platforms/claude-code/legacy-team-runtime.md`
- 文件级迁移记录进入 `docs/legacy-think-tank-full-migration.md`

旧 research agent 已完成 v0.3 全仓迁移处置：

- 7 个旧 agents 映射到 `profiles/`
- 24 个旧 skills 映射到 capabilities、adapter 或 out-of-core
- 私有领域 knowledge 不进入当前主仓，应由具体项目自行维护
- logs、memory、run artifacts 和平台私有配置均有明确处置边界

旧 agent-council 已完成 v0.4 全量迁移处置：

- references、scripts、history 全部逐项归位
- 状态机经验进入 `runtime/council.py`
- HMAC、manifest、原子写入、熔断等工程经验进入 adapter/runtime 迁移文档
- 项目私有上下文不进入 core

v0.5 已补齐专业 subagent runtime 契约：

- `runtime/subagent.py` 生成专业 subagent 任务包、profile prompt 和 role-result 聚合
- `schemas/role-result.schema.json` 固化专业角色输出结构
- `profiles/prompt-pack.md` 将 profiles 转换为可派发 prompt
- Codex 和 Claude Code 均有 specialist runtime 适配说明
- 如果平台没有独立 subagent，必须显式降级为 `single_agent_multi_profile_fallback`

当前本机 Codex 安装验证见：

- `docs/codex-installed-skill-validation.md`
- `docs/codex-external-skills-installation.md`
- `docs/open-source-quickstart.md`
- `docs/support-matrix.md`
- `docs/open-source-release.md`

当前仓库公开发行档：

- `skill_core_only_bundle`

仍未声明完成：

- Claude Code Agent Team
- 真实多 agent 并行执行
- Claude Code adapter 自动 dispatch
- Browser 外部网页 DOM 回收
- `yt-dlp`、`obsidian`、`xiaohongshu` 等外部 skills 集成

## 对外 Quickstart

面向外部用户，建议先读：

1. `docs/open-source-quickstart.md`
2. `docs/support-matrix.md`
3. `docs/validation-tiers.md`
4. `examples/public/research-request.md`
5. `examples/public/council-decision.md`
6. `examples/public/review-acceptance.md`
7. `platforms/codex/operating-guide.md`
8. `docs/open-source-release.md`

推荐最小验证命令：

```bash
python3 checks/open_source_release_suite.py
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/schema_sample_check.py
python3 checks/minimal_runtime_execution_check.py
python3 checks/release_privacy_check.py
python3 checks/open_source_release_check.py
```
