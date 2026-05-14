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
- 增加 MIT License。

### Notes

- 当前版本是主仓基础版本，重点是统一抽象和协议边界。
- 旧 research think-tank 和 agent-council 都被视为 Claude Code 平台旧资产来源。
- 当前不声明真实多 agent runtime 已完成；平台能力必须继续区分 `verified`、`mock`、`tracking`、`planned`。
- 当前不声明 Browser 外部网页 DOM 回收能力；该路径在当前 Codex 环境标记为 `blocked`。
