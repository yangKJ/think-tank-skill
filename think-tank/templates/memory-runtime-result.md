# Memory Runtime Result Template

```yaml
memory_runtime:
  enabled:
  memory_candidates:
    - id:
      layer: episodic | semantic | procedural
      type:
      title:
      summary:
      source_refs: []
      privacy:
      staleness_risk:
      expires_when:
      confidence:
      target:
      action:
  promotion_decisions:
    - candidate_id:
      from:
      to:
      decision:
      reason:
      privacy_review:
        no_secret:
        public_safe:
      staleness_review:
        has_expiry_rule:
        review_after:
      quality_check:
        target_allowed:
        user_confirmed_if_write:
        no_private_core_leak:
  conflicts: []
  written: []
  skipped: []
  boundaries: []
```
