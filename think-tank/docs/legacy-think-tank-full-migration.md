# Legacy Think Tank Full Migration

本文记录旧 Claude Code 版 think-tank 的全量迁移结果。

旧来源：

```text
/Users/condy/Desktop/img-company/agents/research/.claude/skills/think-tank
```

## 结论

```yaml
legacy_think_tank_migration: complete
migration_style: abstracted_not_copied
core_protocol_dependency_on_legacy: none
claude_team_runtime_status: historical_adapter_source
```

旧 think-tank 的价值已经迁移到当前主仓，但迁移方式不是复制旧脚本目录。当前主仓把旧资产拆成：

- 协议层：阶段、角色、共识、质量门禁、结果结构。
- runtime 层：slot resolver、state model、consensus、safety。
- Claude Code 适配层：Agent Team 历史行为、dispatch contract、minimal runtime。
- 模板层：deep research、expert meeting、task kickoff。
- 文档层：配置、安全、故障处理、迁移取舍。

## 文件级处置

| 旧资产 | 新位置 | 处置 |
|--------|--------|------|
| `SKILL.md`、`README.md` | `think-tank/SKILL.md`、`think-tank/README.md` | 重写为跨平台主 Skill，不保留 research 从属关系 |
| `skill.yaml`、`skill.yaml.example` | `protocol/mode-selection.md`、`runtime/planner.py`、`platforms/claude-code/agent-mapping.md` | 抽象为 mode/profile/capability，不保留旧 YAML 作为真相源 |
| `core/workflow.py` | `runtime/planner.py`、`protocol/runtime-contract.md` | 迁移 workflow 选择、阶段规划、严格状态边界 |
| `runtime/slot_resolver.py`、`runtime/slot_validator.py` | `runtime/slot_resolver.py`、`capabilities/slot-contract.md` | 迁移 required/optional slot 语义和缺失能力降级 |
| `core/state.py` | `runtime/state_model.py`、`protocol/state-result-contract.md` | 迁移 run/result/recovery 数据结构，去除旧 `.think-tank/` 绑定 |
| `core/consensus.py` | `runtime/consensus.py`、`protocol/consensus-contract.md` | 迁移 explicit vote、blocking objection、continue/stop |
| `scripts/safe_filename.py`、`prompt_defender.py`、`dangerous_cmd_detector.py`、`data_sanitizer.py` | `runtime/safety.py` | 迁移为平台无关安全 helper |
| `scripts/checkpoint.py`、`concurrency_manager.py`、`heartbeat.py` | `protocol/state-result-contract.md`、`platforms/claude-code/legacy-team-runtime.md` | 迁移为状态/恢复契约，不复制旧文件系统协调器 |
| `scripts/cycle_detector.py` | `runtime/safety.py` | 迁移为 `detect_cycle` |
| `scripts/workflow_router.py` | `runtime/planner.py`、`protocol/mode-selection.md` | 迁移触发和复杂度选择思想 |
| `scripts/agent_config_loader.py`、`config_validator.py`、`validate_config.py` | `platforms/claude-code/agent-mapping.md`、检查脚本 | 迁移“不要硬编码 general-purpose”和配置校验经验 |
| `scripts/orchestrator.py`、`coordinator.py`、`coordinator_agent.py`、`tmux_manager.py` | `platforms/claude-code/legacy-team-runtime.md` | 标记为历史 Claude Team 实现，不进入 core runtime |
| `references/research-protocol.md` | `modes/research.md`、`protocol/quality-gates.md`、`docs/v0.2-runtime-hardening.md` | 迁移来源分级、证据、反方审查、决策日志要求 |
| `references/safety.md` | `runtime/safety.py`、`docs/legacy-runtime-safety.md` | 迁移路径白名单、密钥、prompt injection、Team 清理风险 |
| `references/configuration.md` | `platforms/claude-code/legacy-team-runtime.md` | 迁移 Claude Code 旧配置说明 |
| `references/troubleshooting.md` | `platforms/claude-code/legacy-team-runtime.md` | 迁移 TeamDelete、残留状态、恢复演练经验 |
| `references/conclusion-template.md` | `templates/README.md`、`templates/*.md` | 迁移为跨平台输出模板 |
| `templates/deep-research.md`、`expert-meeting.md`、`task-kickoff.md` | `think-tank/templates/` | 重写为当前协议字段 |
| `.think-tank/` 历史运行结果 | `examples/` 中的精选样例 | 不全量搬迁，避免把旧运行记录当协议真相 |
| `tests/test_think_tank.py` | `checks/*` | 迁移为当前主仓验收脚本 |

## 不迁移为代码的旧实现

以下旧实现不进入当前 core：

- Claude Code Agent Team 私有协调器。
- tmux 进程协调。
- 旧 `.think-tank/inbox`、`outbox`、`shared/results` 文件通信协议。
- 旧运行记录、缓存、pytest cache、pycache。
- 旧 research agent 私有 agent memory。

原因：

- 它们是 Claude Code 特定实现，不是跨平台协议。
- 当前主仓已有 `platforms/claude-code/` 承接这些运行经验。
- 原样复制会让旧妥协实现重新成为中心。

## 完成标准

本次迁移完成后，必须满足：

- 旧 think-tank 没有未分类核心资产。
- 所有可复用能力都有新位置。
- 所有旧 Claude Team 限制都有边界说明。
- 检查脚本能验证迁移后的核心文件存在。
- 不把旧 mock、tracking、direct call 误写成 full verified。

