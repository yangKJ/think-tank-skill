# Public Example: Research To Action

## User Request

把这份竞品调研整理成下一步行动建议，区分哪些现在该做，哪些只需要继续观察。

## Expected think-tank Routing

```yaml
selected_intent: research_to_action
selected_mode: strategy
selected_recipe: research-to-action
selected_profiles:
  - source-collector
  - report-architect
  - product-strategist
  - skeptic
selected_capabilities:
  - source-acquisition
  - knowledge-persistence
skill_route:
  source-acquisition: local_files
  knowledge-persistence: not_selected
execution_method: direct_tool_call
invoked_providers: []
not_invoked_providers:
  - web-access
  - social-listening
  - browser-automation
boundaries:
  - recommendations must separate verified signals from inference
  - observe_only items must not be described as ready to execute
  - no project code or docs are modified automatically
verification_status: verified_for_protocol_example
```

## Output Shape

```text
结论
关键证据
影响判断
行动建议
backlog 候选
风险与边界
```

## Key Rule

Research does not become execution by default. The output must tell the host
agent what is ready, what still needs input, and what should remain in
observation.
