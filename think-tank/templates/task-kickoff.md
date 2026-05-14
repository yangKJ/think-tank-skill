# Task Kickoff

```yaml
mode: "{research|council|review|strategy}"
profiles: "{selected_profiles}"
capabilities: "{selected_capabilities}"
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

## Objective

`{objective}`

## Background

`{background}`

## Success Criteria

- `{criterion}`

## Scope

### In Scope

- `{in_scope_item}`

### Out of Scope

- `{out_of_scope_item}`

## Runtime Plan

```yaml
stages:
  - intake
  - mode_selection
  - role_planning
  - collection
  - independent_analysis
  - deliberation
  - synthesis
  - recommendation
  - quality_check
```

## Capability Plan

```yaml
required_slots:
  - "{capability}"
optional_slots:
  - "{capability}"
fallback_policy: "{fallback_policy}"
```

## Risks

- `{risk}`

## Boundaries

- `{known_boundary}`

## Deliverables

- `{deliverable}`

## Quality Check

```yaml
protocol_complete: true
status_labels_explicit: true
no_mock_claimed_as_verified: true
runtime_provenance_present: true
```
