# Expert Meeting Record

```yaml
mode: council
profiles:
  - facilitator
  - product-strategist
  - skeptic
  - report-architect
capabilities: []
runtime_provenance:
  think_tank_runtime_used: "{true|false}"
  provider_policy_checked: "{true|false}"
  dispatch_decision_emitted: "{true|false}"
  provider_invoked: false
  result_recovered: "{true|false}"
  true_multi_agent_runtime: "{true|false}"
  execution_method: "{full_runtime|single_agent_multi_profile|manual_synthesis|protocol_only}"
  data_collection: "{user_provided|local_files|none}"
  evidence_state: "{selected|recovered|verified_partial|tracking}"
  result_recovery: "{automatic|manual|none}"
  boundaries: []
```

## Topic

`{topic}`

## Decision Context

- background: `{background}`
- decision_needed: `{decision_needed}`
- constraints: `{constraints}`

## Profile Positions

### Facilitator

`{facilitator_summary}`

### Product Strategist

`{product_position}`

### Skeptic

`{skeptic_position}`

### Report Architect

`{report_architect_position}`

## Consensus

- `{consensus_point}`

## Disagreements

- `{disagreement}`

## Blocking Objections

- `{blocking_objection_or_none}`

## Decision

`{decision}`

## Risks

- `{risk}`

## Action Recommendations

```yaml
- owner: "{owner}"
  action: "{action}"
  priority: "{P0|P1|P2}"
  dependency: "{dependency_or_none}"
```

## Boundaries

- `{boundary}`

## Quality Check

```yaml
all_required_profiles_heard: "{true|false}"
blocking_objections_addressed: "{true|false}"
no_external_tool_claim_without_invocation: true
actionable: "{true|false}"
runtime_provenance_present: true
```
