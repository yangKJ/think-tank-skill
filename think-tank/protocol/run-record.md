# Run Record Protocol

Run record is the 2.0 contract for making a think-tank run replayable.

It records what the run tried to do, how it selected mode and profiles, which providers were only selected, which providers were invoked, what evidence was used, what conclusions were produced, and what should happen after the run.

## Goal

```yaml
feature: run_record
version: "2.0"
scope: platform_neutral
default_behavior: emit_structured_record
public_core_stores_private_runs: false
```

## Required Structure

```yaml
run_record:
  run_id:
  created_at:
  user_intent:
  selected_mode:
  selected_recipe:
  selected_profiles: []
  selected_capabilities: []
  runtime_provenance: {}
  provider_invocation_ledger: {}
  evidence_refs: []
  conclusions: []
  disagreements: []
  risks: []
  next_actions: []
  post_run_curation: {}
  memory_runtime: {}
  quality_check: {}
```

## Replay Boundary

A run record is replayable when a future agent can answer:

- What was the user trying to decide or accomplish?
- Which mode, profiles, capabilities, and providers were selected?
- Which providers were actually invoked and recovered?
- What evidence supported each conclusion?
- Which follow-up actions were proposed, written, skipped, or blocked?
- Which memory candidates were generated and how stale they may become?

## Non-Claims

- A run record is not proof that private files, notes, issues, or ledgers were written.
- A run record is not proof that every selected provider was invoked.
- A run record is not a substitute for source evidence, command output, or artifact checks.

## Quality Gate

```yaml
quality_check:
  has_runtime_provenance: true
  has_provider_invocation_ledger: true
  selected_vs_invoked_clear: true
  evidence_refs_present: true
  memory_boundary_clear: true
  post_run_curation_present: true
  private_data_not_published: true
```
