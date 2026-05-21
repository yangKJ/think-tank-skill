# Evidence Recovery Plan

```yaml
evidence_recovery_plan:
  target_question: "{which conclusion or acceptance point needs stronger evidence}"
  current_evidence_state: "{selected|dispatched|invoked|recovered|verified_partial|blocked|failed}"
  confidence: "{low|medium|high}"
  blocking_gap: "{the main missing evidence}"
  target_upgrade_state: "{verified_partial|verified}"
  recovery_actions:
    - action_id: "{action_id}"
      actor: "{host_agent|provider|human}"
      action: "{concrete next action}"
      invocation_required: "{true|false}"
      expected_artifacts:
        - "{artifact_or_evidence}"
      success_condition: "{what proves the gap is closed}"
      failure_behavior: "{how to degrade if this action cannot complete}"
  fallback_if_unavailable: "{what to do if the preferred path is unavailable}"
  boundaries:
    - "{what this plan does not solve}"
```

## Quality Check

```yaml
evidence_recovery_quality_check:
  target_question_explicit: true
  blocking_gap_specific: true
  target_upgrade_state_explicit: true
  action_owner_explicit: true
  invocation_boundary_clear: true
  success_condition_present: true
  fallback_present: true
```
