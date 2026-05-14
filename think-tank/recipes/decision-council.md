# Decision Council Recipe

```yaml
intent: decision_council
default_mode: council
core_question: "多个角色如何审议一个复杂判断并形成可执行结论？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `开会讨论`
- `讨论一下`
- `帮我判断`
- `是否应该`
- `正反意见`
- `观点碰撞`
- `专家组`

## Defaults

```yaml
profiles:
  - facilitator
  - product-strategist
  - skeptic
  - report-architect
capabilities: []
optional_peer_skills: []
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

1. 明确议题和决策标准。
2. 分角色独立观点。
3. 共识、分歧和 blocking objection。
4. 裁决或推荐路径。
5. 后续验证动作。

## Output

```text
结论
角色观点
共识
分歧与风险
裁决
行动建议
边界
```
