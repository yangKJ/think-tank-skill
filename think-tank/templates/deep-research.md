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
runtime_provenance_present: true
```
