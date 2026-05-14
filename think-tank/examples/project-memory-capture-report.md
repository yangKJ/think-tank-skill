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
confidence: high
staleness_risk: low
```

## Decision

This candidate is valid because it has source files, a verification command,
scope, privacy label, and no secret-bearing content.

## Boundary

No public `think-tank/` file is modified by default. A write requires explicit
confirmation.

