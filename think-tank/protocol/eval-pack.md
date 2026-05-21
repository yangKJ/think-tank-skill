# Eval Pack

Eval pack is the 2.0 regression contract for checking that think-tank outputs keep their structure, boundaries, and evidence discipline as the skill evolves.

## Goal

```yaml
feature: eval_pack
version: "2.0"
purpose: prevent protocol regressions
```

## Eval Case Types

```yaml
research:
  checks: mode selection, source boundary, run record, post-run curation
review:
  checks: findings first, release gate, evidence refs, residual risk
council:
  checks: role views, disagreements, consensus, runtime truthfulness
provider_fallback:
  checks: selected_not_invoked, fallback, blocker, verification status
memory_promotion:
  checks: memory layer, privacy, staleness, promotion decision
handoff_guardrail:
  checks: input filter, permission gate, failure boundary
```

## Required Eval Result

```yaml
eval_result:
  eval_id:
  case_type:
  fixture:
  expected_contracts: []
  actual_contracts: []
  passed:
  failures: []
  residual_risk: []
```

## Boundary

Eval pack checks contract shape and known safety boundaries. It does not prove factual correctness for every real-world claim unless the fixture includes evidence and source verification rules.
