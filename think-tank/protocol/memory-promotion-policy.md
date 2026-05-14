# Memory Promotion Policy

Memory promotion decides whether a memory candidate should stay local, move to
project instructions, become project docs, or be generalized into public
think-tank protocol.

## Goal

```yaml
feature: memory_promotion_policy
default_behavior: keep_local_until_reviewed
write_requires_confirmation: true
public_core_requires_generalization: true
```

## Promotion Targets

```yaml
.think-tank/memory/:
  use_for: project-local candidates, run lessons, provider preferences
  privacy_allowed:
    - project_local
    - private
AGENTS.md:
  use_for: local agent behavior rules and repo-specific boundaries
  privacy_allowed:
    - project_local
    - private
project_docs:
  use_for: team-facing docs in the current project
  privacy_allowed:
    - public
    - project_local
think-tank_public_protocol:
  use_for: platform-neutral reusable rules
  privacy_allowed:
    - public
```

## Decision Rules

```yaml
keep_in_local_memory:
  when:
    - project-specific
    - high staleness risk
    - private or user-local preference
promote_to_agents:
  when:
    - affects future agent behavior in this repo
    - has stable project boundary value
promote_to_project_docs:
  when:
    - useful to human maintainers
    - not secret
    - not just an agent instruction
promote_to_public_protocol:
  when:
    - platform-neutral
    - no private path, private project, or private provider preference
    - reusable across projects
    - backed by evidence and quality gates
```

## Rejection Rules

```yaml
reject_public_promotion:
  if:
    - contains private path
    - contains commercial backend detail
    - contains provider preference that belongs to one project
    - contains unverified runtime status
    - lacks expiry rule
```

## Required Promotion Record

```yaml
candidate_id:
from:
to:
decision: keep_local | promote | merge | reject
reason:
privacy_review:
  no_secret:
  public_safe:
staleness_review:
  has_expiry_rule:
  review_after:
evidence:
  files: []
  commands: []
quality_check:
  target_allowed:
  user_confirmed_if_write:
  no_private_core_leak:
```

