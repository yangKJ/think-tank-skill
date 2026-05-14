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
```

