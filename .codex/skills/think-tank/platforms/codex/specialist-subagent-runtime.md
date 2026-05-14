# Codex Specialist Subagent Runtime

本文定义 Codex 平台如何执行 think-tank v0.5 专业 subagent runtime。

## 当前状态

```yaml
codex_specialist_subagent_runtime: specified
true_parallel_subagent_runtime: not_verified
fallback_runtime: supported
```

当前 Codex 主路径可以稳定执行：

- runtime planning
- profile prompt generation
- role-result schema validation
- single-agent multi-profile fallback

但不能在没有明确平台能力时声称多个独立 subagent 已真实并发执行。

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

