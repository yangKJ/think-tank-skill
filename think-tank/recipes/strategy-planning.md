# Strategy Planning Recipe

```yaml
intent: strategy_planning
default_mode: strategy
core_question: "下一阶段路线、优先级和行动方案应该如何安排？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `制定策略`
- `路线图`
- `优先级`
- `行动方案`
- `阶段计划`
- `下一步怎么做`
- `长期演进`

## Defaults

```yaml
profiles:
  - facilitator
  - product-strategist
  - skeptic
  - report-architect
capabilities:
  - source-acquisition
  - knowledge-persistence
# Provider selection is configured in .think-tank/provider-policy.yaml
```

## Runtime Provenance

```yaml
runtime_provenance:
  think_tank_runtime_used: "{true|false}"
  provider_policy_checked: "{true|false}"
  dispatch_decision_emitted: "{true|false}"
  provider_invoked: "{true|false}"
  result_recovered: "{true|false}"
  true_multi_agent_runtime: "{true|false}"
  execution_method: "{full_runtime|adapter_runtime|direct_tool_call|single_agent_multi_profile|manual_synthesis|protocol_only}"
  data_collection: "{provider_managed|direct_assistant_tool|user_provided|local_files|none}"
  evidence_state: "{selected|invoked|recovered|verified_partial|verified|blocked|failed|tracking}"
  result_recovery: "{automatic|manual|none}"
  boundaries: []
```

## Required Analysis

1. 目标和约束。
2. 可选路线。
3. 优先级和阶段切分。
4. 风险、依赖和停止条件。
5. 哪些建议可以直接进入执行，哪些只应观察或等待输入。
6. 可执行计划。

## Output

```text
结论
路线选择
阶段计划
strategy_to_backlog
风险
行动清单
边界
```

## Quality Gates

- 不把长期方向直接包装成当前迭代任务。
- 每个关键动作都应说明 readiness 和主要依赖。
- 如果当前只够支持观察，应明确输出 `observe_only`，而不是伪造执行确定性。
