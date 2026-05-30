# Codex Specialist Subagent Runtime

本文定义 Codex 平台如何执行 think-tank v0.5 专业 subagent runtime。

## 当前状态

```yaml
codex_specialist_subagent_runtime: specified
true_parallel_subagent_runtime: verified_partial_with_scoped_write_lifecycle
fallback_runtime: supported
```

当前 Codex 主路径可以稳定执行：

- runtime planning
- profile prompt generation
- role-result schema validation
- single-agent multi-profile fallback
- independent Codex subagent dispatch for readonly council analysis
- scoped Codex subagent writes with lifecycle continuation

但不能把这次只读 council 验证扩写成所有外部 provider、长期任务生命周期或其他平台的 full runtime verified。

## Execution Contract

当 Codex 平台支持独立 subagent/worker 时：

```text
main agent
  -> plan_subagent_runtime(...)
  -> create SubagentTask per profile
  -> dispatch each task with profile prompt
  -> require role-result schema
  -> aggregate_role_results(...)
  -> consensus/synthesis
```

当 Codex 平台不支持或未验证时：

```yaml
execution_method: single_agent_multi_profile_fallback
specialist_independence: unavailable
authority_level: lower_fallback_single_context
```

## Acceptance

Codex specialist runtime 只有在满足以下条件时才能标记为 verified：

- 每个 profile 有独立 task payload。
- 每个 profile 返回 `role-result`。
- 主 runtime 只汇总返回结果，不伪造缺失结果。
- 输出标注 `execution_method` 和 `authority_level`。

当前 Codex 验收状态：

```yaml
readonly_council_subagents: verified_partial
scoped_write_subagent_lifecycle: verified_partial
external_provider_invocation_inside_subagents: not_verified
long_running_subagent_lifecycle: verified_partial
```

证据：

- `examples/platforms/codex/codex-true-council-runtime.md`
- `docs/codex-true-multi-agent-validation.md`
- `examples/platforms/codex/codex-subagent-lifecycle-validation.md`
