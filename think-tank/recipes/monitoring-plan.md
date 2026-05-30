# Monitoring Plan Recipe

```yaml
intent: monitoring_plan
default_mode: strategy
core_question: "应该持续关注什么、如何监控、什么时候触发行动？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `持续关注`
- `监控方案`
- `定期追踪`
- `每周看一下`
- `有变化提醒我`
- `跟踪动态`

## Defaults

```yaml
profiles:
  - source-collector
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

1. 监控对象。
2. 指标和来源。
3. 频率和阈值。
4. 异常触发条件。
5. 输出格式和行动建议。

## Output

```text
监控目标
指标和来源
频率
触发条件
行动建议
边界
```
