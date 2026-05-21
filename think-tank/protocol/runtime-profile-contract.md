# Runtime Profile Contract

本文定义 think-tank 的运行强度分层：`quick`、`standard`、`deep`。

它解决的问题是：

> 哪些任务只需要轻量增强，哪些任务需要标准审议，哪些任务才值得进入深度研究或完整多阶段 workflow。

## 目的

```yaml
feature: runtime_profile_contract
scope: platform_neutral
purpose: prevent overusing heavy workflows for simple tasks and underusing structure for complex tasks
```

## Profile Summary

```yaml
runtime_profiles:
  quick:
    purpose: "fast structured judgment"
    default_output:
      - skill_route_decision
      - minimal_conclusion
    max_loaded_refs: 3
  standard:
    purpose: "normal think-tank run"
    default_output:
      - task_kickoff_or_mode_output
      - minimal_conclusion
      - evidence_recovery_plan_when_needed
    max_loaded_refs: 8
  deep:
    purpose: "high-stakes, multi-source, or multi-stage run"
    default_output:
      - runtime_plan
      - provider_invocation_ledger_when_providers_are_used
      - run_record
      - minimal_conclusion
      - evidence_recovery_plan_when_needed
    max_loaded_refs: "task_dependent"
```

## Selection Rules

### `quick`

Use `quick` when:

- the task needs structured judgment but not full research
- the user asks for a brief take, triage, or go/no-go direction
- no external provider call is required
- the answer can fit into `minimal_conclusion`

Do not use `quick` when:

- facts are contested
- external information is required
- the result will drive high-risk execution
- multiple roles must produce independent evidence

### `standard`

Use `standard` when:

- the task benefits from role structure, review, or moderate evidence handling
- the output may influence a task packet, review, or project decision
- some evidence is available, but a full deep run would be excessive
- `evidence_recovery_plan` may be useful

This should be the default for non-trivial `review`, `strategy`, and `council` tasks.

### `deep`

Use `deep` when:

- the task needs multi-source research
- the topic is high-stakes, ambiguous, or likely to affect long-term strategy
- provider invocation, source ledger, run record, or repeatable evidence matters
- the user explicitly asks for deep research, full review, or comprehensive comparison

Deep mode should remain deliberate. It is not the default for simple questions.

## Required Output By Profile

```yaml
runtime_profile_output:
  quick:
    required:
      - selected_runtime_profile
      - selection_reason
      - minimal_conclusion
    optional:
      - evidence_recovery_plan
  standard:
    required:
      - selected_runtime_profile
      - selection_reason
      - selected_mode
      - minimal_conclusion
    conditional:
      - evidence_recovery_plan
      - task_kickoff
  deep:
    required:
      - selected_runtime_profile
      - selection_reason
      - runtime_plan
      - run_record
      - minimal_conclusion
    conditional:
      - provider_invocation_ledger
      - evidence_recovery_plan
      - post_run_curation
```

## Loading Budget

```yaml
loading_budget:
  quick:
    start_with:
      - SKILL.md
      - protocol/skill-trigger-intelligence.md
      - protocol/minimal-conclusion-contract.md
    avoid:
      - all profiles
      - all recipes
      - provider routing docs unless needed
  standard:
    start_with:
      - SKILL.md
      - selected mode doc
      - selected recipe
      - minimal conclusion contract
    add_if_needed:
      - evidence recovery contract
      - selected profiles
  deep:
    start_with:
      - SKILL.md
      - runtime contract
      - selected recipe
      - provider invocation ledger when providers are used
      - run record
```

## Stop Conditions

```yaml
stop_conditions:
  quick:
    stop_when:
      - minimal_conclusion_is_actionable
      - no provider_needed
  standard:
    stop_when:
      - decision_or_review_is_actionable
      - evidence_gaps_have_recovery_plan
  deep:
    stop_when:
      - run_record_is_complete
      - provider_results_recovered_or_blocked
      - evidence_state_and_boundaries_are_explicit
```

## Escalation Rules

```yaml
profile_escalation:
  quick_to_standard:
    when:
      - confidence_low
      - material_risk_found
      - user_needs_acceptance_or_task_packet
  standard_to_deep:
    when:
      - external_sources_required
      - provider_invocation_required
      - decision_is_high_stakes
      - repeatability_or_auditability_required
```

## De-escalation Rules

```yaml
profile_deescalation:
  deep_to_standard:
    when:
      - provider_unavailable_and_user_does_not_need_external_sources
      - enough_local_evidence_exists
  standard_to_quick:
    when:
      - task_is_simple
      - user_needs_only_brief_triage
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

## Verification Status

```yaml
runtime_profile_contract_v0_1: specified
project_binding: none
provider_binding: none
intended_use:
  - lightweight_triage
  - standard_review
  - deep_research
  - workflow_cost_control
```
