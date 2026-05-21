# Provider Invocation Ledger

Provider invocation ledger is the 2.0 contract for proving what happened with optional providers.

It extends `capability-evidence-state-machine.md`, `runtime-provenance.md`, and the v1.1 provider integration patterns.

## Goal

```yaml
feature: provider_invocation_ledger
version: "2.0"
purpose: prevent selected providers from being reported as invoked providers
```

## State Chain

```text
candidate
  -> discovered
  -> selected
  -> preflight_checked
  -> dispatched
  -> invoked
  -> recovered
  -> verified_partial | verified | failed | blocked
```

## Required Entry

```yaml
provider_invocation_ledger:
  entries:
    - capability_slot:
      provider_name:
      provider_type:
      state:
      preflight:
        checked:
        result:
        blockers: []
      dispatch:
        decision:
        reason:
        permission_gate:
      invocation:
        invoked:
        command_or_tool_ref:
        started_at:
        completed_at:
      recovery:
        recovered:
        artifact_refs: []
        error:
      verification:
        status:
        evidence_refs: []
        limitations: []
```

## Ledger Rules

- `selected` is not `invoked`.
- selected is not `invoked`
- `preflight_checked` is not `invoked`.
- `invoked` without `recovered` is not a usable result.
- `recovered` without evidence refs is not `verified`.
- `verified_partial` must state scope and limitations.
- blocked providers must be listed with blocker and fallback.

## Public Boundary

The ledger can mention provider names as examples. It must not publish user credentials, login state, private source paths, account identifiers, private URLs, or raw provider outputs that are not public-safe.
