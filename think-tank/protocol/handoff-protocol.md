# Handoff Protocol

Handoff protocol is the 2.0 contract for moving work between profiles, subagents, providers, or platform adapters without leaking irrelevant context or overstating runtime.

## Goal

```yaml
feature: handoff_protocol
version: "2.0"
scope: platform_neutral
true_multi_agent_requires_evidence: true
```

## Handoff Types

```yaml
profile_handoff:
  description: one think-tank profile hands structured context to another profile
subagent_handoff:
  description: platform runtime delegates to another agent or subagent
provider_handoff:
  description: capability slot dispatches to a provider
human_handoff:
  description: user approval, review, or manual execution is required
```

## Required Packet

```yaml
handoff:
  from:
  to:
  type:
  purpose:
  input_filter:
    include: []
    exclude: []
    redactions: []
  evidence_refs: []
  expected_output:
  guardrails: []
  completion_condition:
  runtime_provenance:
```

## Context Filtering

Every handoff must decide what to include and exclude. Do not forward irrelevant tool logs, private account state, secrets, credentials, or stale memory unless the receiving role needs them and they are permitted.

## Truthfulness Boundary

If the current platform only simulates multiple profiles inside one agent, the run must say:

```yaml
true_multi_agent_runtime: false
execution_method: single_agent_multi_profile
```

If a real subagent handoff happened, the run record must include evidence in runtime provenance or provider ledger.
