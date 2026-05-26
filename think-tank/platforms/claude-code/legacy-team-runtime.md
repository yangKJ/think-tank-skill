# Claude Code Legacy Team Runtime

本文记录旧 think-tank 在 Claude Code Agent Team 上的运行经验，以及它在当前主仓里的边界。

**重要更新 (2026-05-24)**：Agent Team Runtime 已通过真实测试验证，具体调用流程和限制已迁移到 `specialist-subagent-runtime.md`。本文仅保留历史背景和设计参考。

## 定位

```yaml
legacy_team_runtime: historical_adapter_source
current_core_protocol: platform_independent
claude_code_agent_team: verified (see specialist-subagent-runtime.md)
```

旧 think-tank 曾依赖 Claude Code Agent Team、sub-agent 文档、inbox/outbox 文件通信、TeamDelete 清理和 `.think-tank/` 运行目录。

当前 think-tank 不把这些机制当成协议真相源。它们只属于 `platforms/claude-code/` 的历史适配经验。

## 旧机制到新边界

| 旧机制 | 新位置 | 当前状态 |
|--------|--------|----------|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | Claude Code 环境前置条件 | documented_only |
| `TeamCreate` / `SendMessage` / `TeamDelete` | `specialist-subagent-runtime.md` | **verified** |
| `subagent_type` 配置 | `agent-mapping.md` | mapped |
| `documents` 渐进加载 | `agent-mapping.md`、`runtime-pipeline.md` | documented |
| `.think-tank/inbox` / `shared/results` | `state-result-contract.md` | abstracted |
| checkpoint / heartbeat | `state-result-contract.md` | abstracted |
| result polling | `runtime-result.schema.json` | abstracted |
| forced critic / objections | `consensus-contract.md` | implemented_in_minimal_runtime |
| Team cleanup | `specialist-subagent-runtime.md` | **verified** |

## 运行时顺序

旧 Agent Team 路径如果未来恢复，必须遵守当前协议顺序：

```text
dispatch_request
  -> dispatch_decision
  -> team_or_tool_invocation
  -> result_recovery
  -> sources[]
  -> evidence[]
  -> boundaries[]
  -> quality_check
```

不得把 `TeamCreate` 成功当成 think-tank 成功。成功只看是否产生符合协议的结果。

## 必须保留的限制声明

Claude Code adapter 不得声明：

```yaml
adapter_dispatch_runtime: verified
automatic_recovery: verified
true_multi_agent_runtime: verified
```

除非已经有可重复的 runtime procedure、真实 invocation log、自动 result recovery 证据和失败路径样例。

## 清理和恢复

旧经验要求：

- 讨论完成后必须清理 Team。
- 等待 shutdown ack 要有超时。
- TeamDelete 失败时必须明确标记为 `cleanup_failed`，不得静默忽略。
- checkpoint 只能恢复状态，不能伪造已完成 evidence。

## 当前验收策略

基于 2026-05-24 真实测试更新：

- ✅ 已验证 TeamCreate / TeamDelete
- ✅ 已验证 TaskCreate
- ✅ 已验证 Agent spawn 并行执行
- ✅ 已验证 SendMessage (subagent→main) 消息回收
- ✅ 已验证 SendMessage (main→subagent) shutdown
- ✅ 已验证 TeamDelete 清理

详细验证记录见 `specialist-subagent-runtime.md`。

## 下一步待验证

- [ ] agent 间 peer-to-peer SendMessage
- [ ] 状态文件协调机制
- [ ] 大规模并发 (5+ agents)
- [ ] 跨 team 通信

