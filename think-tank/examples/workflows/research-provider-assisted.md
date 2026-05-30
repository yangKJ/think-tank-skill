# Workflow Pattern: Provider-Assisted Research

This workflow shows how `think-tank` can organize a research task that may use optional providers. It is a possible usage pattern, not an implementation of those providers.

```yaml
workflow_status:
  pattern_documented: true
  requires_user_environment: true
  provider_execution: optional
```

## Flow

1. Clarify the research question and decision target.
2. Select `research` mode and relevant profiles.
3. Decide whether user-provided files are enough.
4. If external sources are needed, route to `source-acquisition`.
5. Invoke a provider only when preflight and permission pass.
6. Synthesize findings with source quality labels.
7. Output conclusion, evidence, disagreements, risks, and next actions.

## Boundary Block

```yaml
selected_intent: research
selected_mode: research
selected_profiles:
  - source-collector
  - trend-analyst
  - skeptic
selected_capabilities:
  - source-acquisition
skill_route: provider_assisted_research_pattern
execution_method: protocol_first_with_optional_provider
invoked_providers: []
not_invoked_providers:
  - web-access: selected_not_invoked
boundaries:
  - This pattern does not prove provider availability.
  - User-provided material can be sufficient when external access is unavailable.
verification_status: pattern_documented
```
