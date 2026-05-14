# Claude Code Adapter

本文定义 think-tank 在 Claude Code 中的适配方式。

Claude Code 是执行环境，不是协议源。Claude Code adapter 必须遵守 `protocol/`，不能重新定义 think-tank。

## 能力状态

```yaml
adapter: claude-code
adapter_version: 0.1.0
status:
  skill_entrypoint: verified_for_preflight
  single_agent_protocol_execution: verified_for_preflight
  skill_discovery: verified
  capability_auto_mapping: verified_partial_pre_invocation_decision
  external_source_readonly: verified_partial
  adapter_dispatch_attempt: adapter_dispatch_not_executed_verified_partial
  dispatch_contract_validation: verified_partial_with_order_gap
  dispatch_pre_invocation_decision: verified_partial
  subagent_role_execution: planned
  result_recovery_contract: partial_manual_mapping
  legacy_research_asset_migration: planned
  legacy_agent_council_migration: planned
```

## 执行模型

Claude Code adapter 的目标执行流程：

1. 由 `SKILL.md` 触发 think-tank。
2. 根据 `protocol/mode-selection.md` 选择 mode。
3. 根据 `protocol/roles.md` 选择角色。
4. 将角色映射为 Claude Code agent、subagent、任务片段或单 agent 分段执行。
5. 收集每个角色的独立输出。
6. 进入讨论和交叉质询阶段。
7. 汇总结果并执行质量门禁。
8. 输出最终结论和行动建议。

## Dispatch 契约

Claude Code adapter 的最小 dispatch 行为定义在：

```text
think-tank/platforms/claude-code/dispatch-contract.md
```

该契约要求 adapter 在调用外部 skill/tool 前输出 `dispatch_decision`，调用后输出 `dispatch_log`，并将结果回收到 `sources[]` 与 `evidence[]`。

如果只直接调用 WebFetch、WebSearch 或其他工具，而没有 `dispatch_decision` 和 `dispatch_log`，只能标记为 `verified_partial`，不能标记为完整 adapter dispatch。

## 真实执行要求

Claude Code adapter 必须明确区分：

- agent 是否真实启动
- agent 结果是否真实回收
- 中间结果是否可追踪
- 失败后是否可恢复
- 最终输出是否基于真实角色结果

如果只记录任务状态但没有真实执行或结果回收，必须标注为 `tracking`，不能标注为 `verified`。

## 旧资产迁移

旧 research think-tank 资产可以迁入：

- `modes/research.md`
- `protocol/`
- `platforms/claude-code/`
- `examples/`

旧 agent-council 资产可以迁入：

- `modes/council.md`
- `protocol/roles.md`
- `protocol/quality-gates.md`
- `platforms/claude-code/`

迁移时必须抽象为 think-tank 资产，不能保留旧体系的父级关系。

## 输出要求

Claude Code 输出应遵守主协议输出结构：

- 结论
- 依据
- 角色观点
- 分歧与风险
- 行动建议
- 边界

如果涉及代码修改，还应说明修改文件、验证命令和残余风险。

## 禁止行为

- 不把旧 research skill 当成 think-tank 父级。
- 不把 agent-council 作为平行主线继续扩展。
- 不把 mock 路径包装成真实 Claude Code Team 能力。
- 不把 tracking-only 执行说成已完成多 agent 执行。
