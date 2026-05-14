# Evidence Table

```yaml
mode: research
profiles:
  - source-collector
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

| Claim | Evidence | Source | Authority | Freshness | Confidence | Gaps |
|-------|----------|--------|-----------|-----------|------------|------|
| `{claim}` | `{evidence}` | `{source}` | `A|B|C` | `{date}` | `low|medium|high` | `{gap}` |

## Risks

- `{risk_from_weak_or_missing_evidence}`

## Boundaries

- `{unverified_claim_or_source_limit}`

## Authority Rules

- `A`: official, primary, or independently cross-verified source.
- `B`: credible secondary source.
- `C`: single weak source, forum/social sample, or unverified opinion.

## Quality Check

```yaml
every_claim_has_source: true
authority_labeled: true
confidence_labeled: true
gaps_visible: true
runtime_provenance_present: true
```
