# Research OS

Research OS is the 2.0 project-local workspace model for long-running research, strategy, review, and memory workflows.

The public skill defines the structure and contracts. A user's actual `.think-tank/` workspace is local and should not be committed by default.

## Goal

```yaml
feature: research_os
version: "2.0"
public_core_defines_contract: true
local_workspace_stores_project_data: true
```

## Workspace Layout

```text
.think-tank/
├── inbox/
├── sources/
│   └── ledger.jsonl
├── artifacts/
├── decisions/
├── experiments/
├── runbooks/
├── memory/
├── runs/
└── provider-ledger/
```

## Directory Responsibilities

```yaml
inbox:
  use_for: raw user drops, temporary notes, unsorted source leads
sources:
  use_for: source ledger, source metadata, attribution and freshness
  canonical_file: sources/ledger.jsonl
artifacts:
  use_for: durable reports, briefs, generated samples, exported bundles
decisions:
  use_for: accepted decisions, rationale, alternatives, date and owner
experiments:
  use_for: hypotheses, test plans, results, next decisions
runbooks:
  use_for: repeatable procedures and verification commands
memory:
  use_for: reviewed project memory candidates and promoted local memory
runs:
  use_for: run records and replay metadata
provider-ledger:
  use_for: provider invocation ledgers and recovery evidence
```

## Public Boundary

- The public repository may include templates and schemas.
- The user project owns actual `.think-tank/` contents.
- Private source ledgers, run records, memory candidates, and provider evidence should not be published unless reviewed and intentionally exported.
