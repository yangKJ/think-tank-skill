# Runtime Profile Decision

```yaml
runtime_profile_decision:
  selected_runtime_profile: "{quick|standard|deep}"
  selection_reason: "{why this profile is enough}"
  selected_mode: "{research|council|review|strategy}"
  expected_outputs:
    - "{minimal_conclusion|task_kickoff|run_record|evidence_recovery_plan}"
  loading_budget:
    refs_to_load:
      - "{reference}"
    refs_to_skip:
      - "{reference}"
  escalation_boundary: "{when to move to a heavier profile}"
```

## Quality Check

```yaml
runtime_profile_quality_check:
  selected_runtime_profile_explicit: true
  selection_reason_present: true
  output_matches_profile: true
  loading_budget_respected: true
  escalation_boundary_clear: true
```
