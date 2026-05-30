# Technical Research Recipe

```yaml
intent: technical_research
default_mode: research
core_question: "某项技术、方案或架构是否可行，应该如何落地？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `技术调研`
- `方案调研`
- `可行性分析`
- `架构方案`
- `实现路径`
- `选型`
- `性能/成本/风险`

## Defaults

```yaml
profiles:
  - source-collector
  - trend-analyst
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

1. 技术原理和适用边界。
2. 实现路径和依赖条件。
3. 性能、成本、维护和安全风险。
4. 替代方案比较。
5. 推荐方案和验证步骤。

## Output

```text
结论
方案概述
依据
替代方案
风险
落地步骤
边界
```
