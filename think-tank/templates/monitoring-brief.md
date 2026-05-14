# Monitoring Brief

```yaml
mode: research
research_depth: continuous_monitoring
profiles:
  - source-collector
  - trend-analyst
  - skeptic
capabilities:
  - source-acquisition
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

## Monitoring Topic

`{topic}`

## Time Window

```yaml
from: "{start_time}"
to: "{end_time}"
freshness_required: true
```

## Signals

```yaml
- source: "{source}"
  signal: "{signal}"
  strength: "{low|medium|high}"
  evidence: "{evidence}"
  changed_since_last_check: "{true|false|unknown}"
```

## Key Changes

- `{change}`

## No-Change Areas

- `{area}`

## Risks

- `{risk}`

## Boundaries

- `{unverified_or_unavailable_source}`

## Next Check

```yaml
trigger: "{time_or_event}"
watch_items:
  - "{watch_item}"
```

## Quality Check

```yaml
source_window_clear: true
changes_separated_from_baseline: true
no_unverified_alert_claim: true
runtime_provenance_present: true
```
