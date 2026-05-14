# Capability Evidence State Machine

Capability status must describe the strongest evidence actually observed. It
must not describe intent, hope, or a nearby successful path.

## Goal

```yaml
feature: capability_evidence_state_machine
scope: protocol
purpose: prevent installed, selected, invoked, recovered, and verified from being conflated
```

## States

```yaml
planned:
  meaning: documented future capability; no current runtime evidence
mock:
  meaning: exercised only through fake, fixture, or manually simulated path
installed:
  meaning: provider files or tool entrypoints exist in the current environment
discovered:
  meaning: platform adapter found the provider and read its metadata
selected:
  meaning: policy or planner selected the provider for a request
dispatched:
  meaning: dispatch decision was produced before invocation
invoked:
  meaning: provider/tool was actually called
recovered:
  meaning: provider output was mapped into think-tank output contract
verified_partial:
  meaning: a real path worked, but scope is limited or manual steps remain
verified:
  meaning: repeatable runtime procedure exists, output is recovered, and quality gates pass
blocked:
  meaning: capability cannot proceed in the current environment or constraints
failed:
  meaning: provider was invoked and failed
tracking:
  meaning: status is being recorded, but does not prove execution
```

## Ordered Evidence Chain

For a normal provider-backed capability, the strongest path is:

```text
planned
  -> installed
  -> discovered
  -> selected
  -> dispatched
  -> invoked
  -> recovered
  -> verified_partial
  -> verified
```

`mock`, `blocked`, `failed`, and `tracking` are side states. They must not be
silently promoted to `verified`.

## Promotion Rules

```yaml
installed_to_discovered:
  requires:
    - provider metadata or entrypoint read by adapter
discovered_to_selected:
  requires:
    - policy_route or planner decision
selected_to_dispatched:
  requires:
    - dispatch_decision emitted before invocation
dispatched_to_invoked:
  requires:
    - actual tool or provider call
invoked_to_recovered:
  requires:
    - output mapped into sources, evidence, role_result, artifact, or runtime_result
recovered_to_verified_partial:
  requires:
    - real output
    - explicit constraints and boundaries
verified_partial_to_verified:
  requires:
    - repeatable procedure
    - automated or documented recovery
    - quality gates pass
    - failure/degradation behavior documented
```

## Anti-Claims

These claims are forbidden:

```yaml
selected_means_invoked: false
installed_means_usable: false
mock_means_verified: false
manual_recovery_means_automatic_recovery: false
single_success_means_full_runtime_verified: false
```

## Required Output Fields

```yaml
capability:
provider:
state:
evidence:
  files: []
  commands: []
  runtime_logs: []
observed_at:
scope:
boundaries: []
next_required_evidence:
quality_check:
  no_state_inflation: true
  evidence_matches_state: true
  boundaries_present: true
```

