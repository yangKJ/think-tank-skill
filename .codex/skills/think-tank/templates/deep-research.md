# Deep Research Report

```yaml
mode: research
profiles:
  - source-collector
  - trend-analyst
  - report-architect
  - skeptic
capabilities:
  - source-acquisition
  - browser-automation
```

## Task

- objective: `{objective}`
- context: `{context}`
- constraints: `{constraints}`

## Sources

`sources[]`:

```yaml
- title: "{title}"
  url: "{url_or_artifact}"
  source_type: "{source_type}"
  summary: "{summary}"
  reliability: "{low|medium|high}"
  freshness: "{freshness}"
  extracted_at: "{timestamp}"
```

## Evidence

- `{evidence_item_1}`
- `{evidence_item_2}`

## Analysis

### Source Collector

`{source_collector_findings}`

### Trend Analyst

`{trend_analyst_findings}`

### Skeptic

`{skeptic_objections}`

### Report Architect

`{synthesis}`

## Disagreements

- `{disagreement_or_unknown}`

## Risks

- `{risk}`

## Boundaries

- `{unverified_or_blocked_boundary}`

## Action Recommendations

```yaml
- priority: P0
  action: "{action}"
  rationale: "{rationale}"
```

## Quality Check

```yaml
protocol_complete: "{true|false}"
evidence_boundary_clear: "{true|false}"
no_full_runtime_overclaim: true
actionable: "{true|false}"
```

