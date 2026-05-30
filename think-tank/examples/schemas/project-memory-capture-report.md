# Project Memory Capture Report

```yaml
selected_recipe: project-memory-capture
default_behavior: propose_only
write_requires_confirmation: true
target_workspace: .think-tank/
```

## Candidate

```yaml
id: provider-selection-not-invocation
type: workflow
target: .think-tank/memory/workflows.md
privacy: project_local
action: append
status: active
confidence: high
staleness_risk: low
expires_when: User changes the project policy model or provider invocation contract.
review_after: null
refresh_trigger:
  - Before changing provider policy runtime semantics.
  - When provider invocation matrix or routing checks change.
```

## Decision

This candidate is valid because it has source files, a verification command,
scope, privacy label, and no secret-bearing content.

## Boundary

No public `think-tank/` file is modified by default. A write requires explicit
confirmation.
