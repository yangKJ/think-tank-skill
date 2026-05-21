# Workflow Pattern: Council Release Decision

This workflow shows how `think-tank` can structure a release decision council. It is not a claim of true multi-agent runtime unless the platform reports subagent invocation evidence.

```yaml
workflow_status:
  pattern_documented: true
  true_multi_agent_runtime: depends_on_platform_evidence
  provider_execution: optional
```

## Flow

1. State the release decision and acceptance criteria.
2. Select `council` mode.
3. Assign profiles for product, engineering, risk, and evidence review.
4. Gather repo evidence and release gate output.
5. Separate agreement, disagreement, residual risk, and required actions.
6. Declare whether the council was single-agent multi-profile or true subagent runtime.

## Boundary Block

```yaml
selected_intent: decision_council
selected_mode: council
selected_profiles:
  - product-strategist
  - report-architect
  - skeptic
selected_capabilities:
  - evidence-synthesis
skill_route: council_release_decision_pattern
execution_method: protocol_first_council
invoked_providers: []
not_invoked_providers: []
boundaries:
  - Single-agent multi-profile reasoning is not true multi-agent runtime.
  - Release approval requires evidence from checks, examples, or explicit review.
verification_status: pattern_documented
```
