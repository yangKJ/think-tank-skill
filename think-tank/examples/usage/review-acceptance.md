# Public Example: Review Acceptance

## User Request

审查这次 PR 是否可以作为公开发布候选，重点看隐私泄漏、文档承诺和验证命令是否一致。

## Expected think-tank Routing

```yaml
selected_intent: review_acceptance
selected_mode: review
selected_recipe: review-acceptance
selected_profiles:
  - skeptic
  - report-architect
  - product-strategist
selected_capabilities:
  - source-acquisition
skill_route:
  source-acquisition: local_files
execution_method: direct_tool_call
invoked_providers: []
not_invoked_providers:
  - web-access
  - social-listening
  - knowledge-persistence
boundaries:
  - findings must cite files and lines
  - release readiness requires checks to pass
  - no remote publish action is performed
verification_status: verified_for_protocol_example
```

## Output Shape

```text
Findings
Open Questions
Change Summary
Verification
Release Boundary
```

## Key Rule

Review findings lead. Summaries and release confidence come after concrete evidence.
