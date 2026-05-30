# Workflow Pattern: Open Source Readiness Review

This workflow shows how `think-tank` can organize an open-source readiness review. It is a possible review pattern, not a guarantee that a repository is publishable.

```yaml
workflow_status:
  pattern_documented: true
  requires_repo_evidence: true
  provider_execution: optional
```

## Flow

1. Review public package scope.
2. Check ignored private paths and release manifest.
3. Check README, examples, license, contribution docs, and validation commands.
4. Search for overclaims about optional providers.
5. Run release gates when available.
6. Produce findings first, then residual risk and action list.

## Boundary Block

```yaml
selected_intent: review_acceptance
selected_mode: review
selected_profiles:
  - skeptic
  - report-architect
selected_capabilities:
  - artifact-review
  - release-gate
skill_route: open_source_readiness_pattern
execution_method: protocol_first_review
invoked_providers: []
not_invoked_providers: []
boundaries:
  - Passing a local gate is evidence, not a substitute for maintainer review.
  - Optional providers must be documented as patterns unless invocation evidence exists.
verification_status: pattern_documented
```
