# Changelog

本文件记录 think-tank-skill 仓库和 think-tank 协议的公开演进。

格式参考 Keep a Changelog，版本遵循语义化版本。

## [0.1.0] - 2026-05-14

### Added

- 建立 `think-tank/` 作为唯一主 Skill 目录。
- 建立协议层：`protocol/`。
- 建立平台适配层：`platforms/claude-code/` 和 `platforms/codex/`。
- 建立场景模式层：`modes/research.md`、`modes/council.md`、`modes/review.md`、`modes/strategy.md`。
- 建立旧资产迁移说明：research think-tank 和 agent-council。
- 建立 Claude Code runtime contract 初稿。
- 完成 Codex 四个核心 mode 的 foundation 验证。
- 增加 Codex 验收文档和验证脚本。
- 增加 capability 降级验证和 Browser optional localhost fixture 验证记录。
- 增加 JSON schema 输入输出样例和样例检查脚本。
- 增加 Codex 主平台运行手册、任务模板和 capability 状态矩阵。
- 验证 Codex 本地 source-acquisition 与 Markdown artifact 闭环。
- 验证 Codex 外部只读 source-acquisition，并将 Browser 外部 DOM 回收标记为 blocked。
- 增加 Codex readiness matrix，明确进入 Claude Code preflight 前的停止点。
- 记录 Claude Code research mode preflight 首轮验证，状态为 `verified_with_format_gap`。
- 记录 Claude Code council mode preflight 首轮验证，状态为 `verified_as_single_agent_council_preflight`。
- 记录 Claude Code capability discovery 验证；skill discovery 为 `verified`，capability 自动调度仍为 `mock/planned`。
- 记录 Claude Code WebFetch 外部只读 source-acquisition 片段验证，状态为 `verified_partial`。
- 记录 Claude Code adapter dispatch 尝试，结论为直接 WebFetch 调用，adapter dispatch 未发生。
- 增加 Claude Code dispatch contract 和目标输出样例。
- 将 Claude Code dispatch contract 接入 `SKILL.md` 执行规则，并增加 dispatch 验证提示词。
- 增加 Claude Code dispatch JSON schema、机器可检查样例和检查脚本。
- 记录 Claude Code dispatch contract 验证，状态为 `verified_partial_with_order_gap`。
- 记录 Claude Code pre-invocation dispatch decision 验证，`capability_auto_mapping` 提升为 `verified_partial_pre_invocation_decision`。
- 增加 v0.1 foundation final 收口文档。
- 增加 Claude Code minimal runtime 约定、schema、成功/失败样例和检查脚本。
- 增加 Codex minimal runtime mirror、参考 runner、成功/失败样例和执行检查脚本。
- 增加 capability 验证队列检查脚本和最终验收计划。
- 记录 Claude Code final low-flow validation，状态为 `verified_partial_with_success_pre_invocation_and_failure_degradation`。
- 增加 v0.2 runtime hardening 契约：runtime、state/result、slot、consensus 和 research hardening。
- 增加 v0.2 四个检查脚本：`runtime_contract_check.py`、`slot_contract_check.py`、`consensus_contract_check.py`、`research_protocol_check.py`。
- 增加 v0.2 平台无关 minimal runtime library：planner、slot resolver、state model、consensus evaluator。
- 增加 v0.2 runtime 实现检查脚本：`runtime_planner_check.py`、`slot_resolver_check.py`、`state_model_check.py`、`consensus_runtime_check.py`。
- 增加 v0.2 adapter integration：平台无关 `runtime-result.schema.json`、Codex runtime pipeline、Claude Code runtime pipeline spec 和 E2E fixture。
- 增加 adapter integration 检查脚本：`runtime_result_schema_check.py`、`codex_runtime_pipeline_check.py`、`claude_runtime_pipeline_spec_check.py`、`runtime_e2e_fixture_check.py`。
- 增加 optional capability 后续验证路线图。
- 完成旧 Claude Code 版 think-tank 全量迁移处置文档，明确每类旧文件的新位置和不原样复制原因。
- 增加 `runtime/safety.py`，迁移旧安全文件名、危险命令、敏感信息清理、prompt injection 和循环检测能力。
- 增加 `templates/`，迁移并重写旧 deep research、expert meeting、task kickoff 模板为跨平台协议模板。
- 增加 Claude Code legacy Team runtime 文档，保留旧 TeamCreate/TeamDelete/checkpoint/heartbeat 经验但不把它们写进 core protocol。
- 增加旧 think-tank 迁移、安全 runtime 和模板检查脚本。
- 完成 v0.3 旧 research agent 全仓迁移处置：7 个 agents、25 个 skills、35 个 knowledge 文件、logs、memory 和平台私有配置全部归类。
- 增加 `docs/research-agent-full-inventory.md`、`docs/external-skill-interoperability.md`、`docs/v0.3-research-agent-migration.md`。
- 增加 `domain-packs/image-editing/legacy-knowledge-index.md`，将旧 knowledge 作为领域包素材索引而非 core 依赖。
- 增加 `templates/monitoring-brief.md` 和 `templates/evidence-table.md`，迁移旧 daily briefing、shared results 和证据表输出形态。
- 增加 `checks/research_agent_full_migration_check.py`，确保旧 research agent 资产没有未处置项。
- 完成 v0.4 旧 agent-council 全量迁移处置：references、scripts、history、状态机、安全机制和研究子系统全部归类。
- 增加 `runtime/council.py`，迁移旧 collect/discuss/conclude/complete 状态 helper 和 L1/L2/L3 触发判断。
- 增加 `docs/agent-council-full-inventory.md`、`docs/agent-council-runtime-migration.md`、`docs/agent-council-history-index.md`、`docs/v0.4-agent-council-migration.md`。
- 增加 `templates/council-state.md` 和 v0.4 检查脚本：`agent_council_full_migration_check.py`、`council_runtime_check.py`。
- 增加 v0.5 专业 subagent runtime 契约、runtime helper、role-result schema、profile prompt pack 和平台适配说明。
- 增加 `runtime/subagent.py`，支持生成专业 profile task、profile prompt、role result 聚合和 fallback 标签。
- 增加 `schemas/role-result.schema.json`、`examples/specialist-runtime-fixture.json` 和 v0.5 检查脚本。
- 增加 Codex 本机安装验证文档和 `codex_installed_skill_check.py`。
- 将旧 research agent 工具型 skills 作为 Codex 同级 skills 安装，并增加安装清单和 `codex_external_skills_check.py`。
- 增加 MIT License。

### Notes

- 当前版本是主仓基础版本，重点是统一抽象和协议边界。
- 旧 research think-tank 和 agent-council 都被视为 Claude Code 平台旧资产来源。
- 当前不声明真实多 agent runtime 已完成；平台能力必须继续区分 `verified`、`mock`、`tracking`、`planned`。
- 当前不声明 Browser 外部网页 DOM 回收能力；该路径在当前 Codex 环境标记为 `blocked`。
