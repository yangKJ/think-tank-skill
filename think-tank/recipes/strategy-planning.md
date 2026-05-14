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
optional_peer_skills:
  - taskflow
  - obsidian
  - knowledge-graph-builder
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
5. 可执行计划。

## Output

```text
结论
路线选择
阶段计划
风险
行动清单
边界
```
