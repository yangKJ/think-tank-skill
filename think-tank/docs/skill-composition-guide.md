# Skill Composition Guide

think-tank is the coordinating skill. Peer skills and tools provide concrete
execution.

The same boundary always applies: selection is not invocation.

## Responsibility Split

```text
think-tank:
  task understanding
  intent and mode selection
  role organization
  capability slot selection
  dispatch decision structure
  evidence synthesis
  boundary disclosure

peer skills:
  web search
  browser automation
  media download or processing
  social platform access
  knowledge-base read or write
  image, audio, or video production
```

## Composition Flow

```text
user goal
  -> skill_route_decision
  -> invocation contract
  -> selected intent/mode/recipe
  -> capability slot
  -> provider policy
  -> dispatch decision
  -> provider invocation or fallback
  -> result recovery
  -> final synthesis
```

## Common Patterns

### Research With Web Access

Use `think-tank` for research framing, source requirements, role review, and
synthesis. Use a web/search provider only after the task requires current or
external information.

### Review With No Provider

Use `think-tank` for reviewer profiles, acceptance criteria, risk ordering, and
boundary disclosure. Do not route to providers if local files are enough.

### Knowledge Persistence

Use `think-tank` to decide what should become memory. Use a knowledge provider
only after the user permits private writes and the destination is clear.

### Media Or Social Analysis

Use `think-tank` for research questions, evidence schema, and final synthesis.
Use media or social providers only when rights, login state, platform limits,
and user permission are clear.

## Composition Contract

Every composed run should preserve:

```yaml
selected_capability:
candidate_providers:
selected_provider:
preflight_result:
dispatch_decision:
invocation_status:
result_recovery:
fallback_used:
verification_status:
```

## What Not To Do

- Do not make peer skills hard dependencies of the public core.
- Do not hard-code a provider name into a protocol file.
- Do not present provider examples as available on every machine.
- Do not let a peer skill overwrite the final think-tank output structure.
