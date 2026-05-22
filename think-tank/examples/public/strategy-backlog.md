# Public Example: Strategy Backlog

## User Request

基于这轮策略讨论，整理一组可执行 backlog 候选，并标记每项当前是否 ready。

## Expected think-tank Routing

```yaml
selected_intent: strategy_planning
selected_mode: strategy
selected_recipe: strategy-planning
selected_profiles:
  - facilitator
  - product-strategist
  - skeptic
  - report-architect
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
  - each backlog candidate must include readiness and next_owner
  - observe_only items stay out of active execution
  - backlog output is a candidate set, not a claim of implementation
verification_status: verified_for_protocol_example
```

## Output Shape

```text
结论
路线选择
阶段计划
strategy_to_backlog
风险
行动清单
边界
```

## Key Rule

Backlog candidates are only useful when the host agent can immediately see
readiness, owner, dependencies, and validation plan.
