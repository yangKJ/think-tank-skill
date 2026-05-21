# Project Memory Runtime

Project memory runtime is the 2.0 contract for turning run results into reviewed, scoped, and stale-aware memory candidates.

It extends `memory-curation.md` and `memory-promotion-policy.md`. It does not replace them.

## Goal

```yaml
feature: project_memory_runtime
version: "2.0"
default_behavior: propose_then_review
write_requires_confirmation: true
public_core_stores_private_memory: false
```

## Memory Layers

```yaml
episodic:
  use_for: run-specific observations, decisions, blockers, and artifacts
semantic:
  use_for: stable project facts, domain conclusions, reusable source summaries
procedural:
  use_for: repeatable workflows, commands, quality gates, provider decision trees
```

## Runtime Flow

```text
run_result
  -> extract_memory_candidates
  -> classify_layer
  -> attach_sources
  -> privacy_review
  -> staleness_review
  -> conflict_check
  -> promotion_decision
  -> write_if_confirmed
  -> emit_memory_runtime_result
```

## Conflict Rules

```yaml
conflict_check:
  detect_same_topic: true
  compare_scope: true
  compare_freshness: true
  compare_source_strength: true
  allowed_decisions:
    - keep_both
    - supersede_old
    - merge
    - reject_new
    - needs_user_review
```

## Required Result

```yaml
memory_runtime:
  enabled: true
  memory_candidates: []
  promotion_decisions: []
  conflicts: []
  written: []
  skipped: []
  boundaries: []
```

## Boundary

Project memory can land in `.think-tank/`, AGENTS files, project docs, or an external note system only when the current platform has permission and the user confirms writes when required.

Public think-tank core may document the protocol, but it must not store user project memory.
