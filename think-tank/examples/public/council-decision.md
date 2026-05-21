# Public Example: Council Decision

## User Request

开会讨论：团队是否应该把当前内部工作流沉淀为公开 skill。

## Expected think-tank Routing

```yaml
selected_intent: decision_council
selected_mode: council
selected_recipe: decision-council
selected_profiles:
  - facilitator
  - product-strategist
  - skeptic
  - report-architect
selected_capabilities: []
skill_route:
  council-deliberation: core_protocol
execution_method: single_agent_multi_profile_fallback
invoked_providers: []
not_invoked_providers:
  - external-subagents
  - browser-automation
  - private-knowledge-base
boundaries:
  - role labels are perspectives, not independent subagent execution
  - no private implementation details should enter public artifacts
verification_status: verified_for_protocol_example
```

## Output Shape

```text
结论
赞成观点
反对观点
分歧
风险
行动建议
边界
```

## Key Rule

Do not say `true_multi_agent_runtime: true` unless independent agents were actually dispatched and their role results were recovered.
