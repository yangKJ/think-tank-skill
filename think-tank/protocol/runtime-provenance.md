# Runtime Provenance Gate

Every think-tank-style output must disclose how it was produced before it
presents conclusions. A report that looks like think-tank must not hide whether
it came from a full runtime, adapter runtime, direct assistant tool use, or
single-agent profile simulation.

## Goal

```yaml
feature: runtime_provenance_gate
scope: all_think_tank_outputs
purpose: prevent think-tank-shaped reports from overstating runtime execution
```

## Required Block

```yaml
runtime_provenance:
  think_tank_runtime_used: true | false
  provider_policy_checked: true | false
  dispatch_decision_emitted: true | false
  provider_invoked: true | false
  result_recovered: true | false
  true_multi_agent_runtime: true | false
  execution_method: full_runtime | adapter_runtime | direct_tool_call | single_agent_multi_profile | manual_synthesis | protocol_only
  data_collection: provider_managed | direct_assistant_tool | user_provided | local_files | none
  evidence_state: planned | mock | installed | discovered | selected | dispatched | invoked | recovered | verified_partial | verified | blocked | failed | tracking
  result_recovery: automatic | manual | none
  boundaries: []
```

## Disclosure Rules

```yaml
direct_assistant_tool:
  must_say:
    think_tank_runtime_used: false
    data_collection: direct_assistant_tool
    result_recovery: manual
  must_not_say:
    provider_managed: true
    verified: true
single_agent_multi_profile:
  must_say:
    true_multi_agent_runtime: false
  must_not_say:
    independent_subagents: true
provider_selection_only:
  must_say:
    provider_invoked: false
    result_recovered: false
    evidence_state: selected
full_runtime_claim:
  requires:
    - provider_policy_checked: true
    - dispatch_decision_emitted: true
    - provider_invoked: true
    - result_recovered: true
    - evidence_state: verified_partial | verified
```

## Forbidden Claims

```yaml
think_tank_style_implies_runtime: false
role_labels_imply_subagents: false
direct_web_search_implies_source_acquisition_provider: false
manual_synthesis_implies_result_recovery_contract: false
```

## Quality Check

```yaml
runtime_provenance_present: true
execution_method_clear: true
data_collection_clear: true
multi_agent_truthful: true
provider_invocation_truthful: true
recovery_truthful: true
```

