# Memory Curation Protocol

Memory curation turns a think-tank run into reusable project-local knowledge.
It is not automatic note-taking. It is a gated process for verified, scoped,
privacy-labeled knowledge.

## Goal

```yaml
feature: project_memory_capture
scope: project_local
default_behavior: propose_only
write_requires_confirmation: true
public_core_stores_private_memory: false
```

## Memory Types

```yaml
architecture:
  description: project structure, module boundaries, runtime paths
workflow:
  description: commands, test flows, release flows, acceptance procedures
convention:
  description: coding style, naming, directory, team preferences
pitfall:
  description: common mistakes, historical bugs, misleading paths
decision:
  description: architecture, product, protocol, or process decisions
```

## Candidate Lifecycle

```text
collect_candidate
  -> classify
  -> verify_source
  -> privacy_check
  -> deduplicate
  -> propose_patch
  -> write_if_confirmed
  -> report
```

## Memory Item Contract

Every item must include:

```yaml
id:
type:
title:
summary:
source:
  files: []
  commands: []
  discussions: []
verified_at:
scope: repo | module | platform | user_local
privacy: public | project_local | private
staleness_risk: low | medium | high
confidence: low | medium | high
target:
action: append | merge | skip
```

## Target Rules

Allowed target kinds:

```yaml
AGENTS.md:
  use_for: agent behavior rules, project boundaries, current phase
.think-tank/memory/:
  use_for: structured local project memory
project-local skill:
  use_for: reusable local project skill behavior
docs/:
  use_for: public team documentation only when explicitly requested
```

Forbidden by default:

```yaml
forbidden_targets:
  - think-tank/
  - public docs without user request
  - closed-source implementation details
```

## Quality Gates

```yaml
has_source: true
has_scope: true
has_privacy_label: true
has_staleness_risk: true
no_secret: true
no_unverified_claim_as_fact: true
no_duplicate: true
write_requires_confirmation: true
```

## Forbidden Memory

Do not store:

- Temporary status that only mattered in one run.
- Unverified guesses.
- Secrets, tokens, credentials, account identifiers.
- Closed-source commercial backend implementation details.
- Private project paths in public Skill files.
- Personal preferences that belong in a user-local policy.

## Output Contract

The recipe must output:

```yaml
memory_candidates:
  - id:
    type:
    title:
    summary:
    source:
    target:
    action:
    quality_check:
written:
  - id:
skipped:
  - id:
    reason:
boundaries:
  - ...
```

