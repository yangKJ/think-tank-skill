# Council State Template

```yaml
mode: council
runtime_state: council
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

## Selected Profiles

```yaml
profiles:
  - "{profile_a}"
  - "{profile_b}"
  - "{profile_c_optional}"
```

## State

```yaml
phase: collect | discuss | conclude | complete
round: 0
agents_completed: []
consensus_level: none | L1 | L2 | L3
consensus_support: 0.0
final_decision: null
boundaries: []
```

## Collection

- `{profile}`: `{finding_summary}`

## Discussion

```yaml
- round: 1
  profile: "{profile}"
  based_on_facts: "{facts}"
  position: "{position}"
  evidence: []
  objections: []
  vote: agree | disagree | abstain
```

## Synthesis

```yaml
consensus: []
disagreements: []
final_decision: null
recommendations: []
minority_opinions: []
```

## Risks

- `{risk}`

## Boundaries

- `{boundary}`

## Quality Check

```yaml
host_stayed_neutral: true
all_selected_profiles_heard: true
blocking_objections_recorded: true
no_l1_with_blocking_objection: true
ios_project_context_removed: true
runtime_provenance_present: true
```
