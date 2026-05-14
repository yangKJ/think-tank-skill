# Evidence Table

```yaml
mode: research
profiles:
  - source-collector
  - skeptic
capabilities:
  - source-acquisition
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
```
