# Operator Manual

![Operator manual](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/operator-manual-image2.png)

This manual explains how to operate `think-tank` as a high-level collaboration
skill instead of a generic prompt.

## Core Mental Model

```text
think-tank
  = task understanding
  + mode selection
  + role organization
  + capability routing
  + evidence synthesis
  + boundary declaration
```

Optional peer skills perform concrete execution. `think-tank` frames, routes,
verifies, and summarizes.

## When To Use It

Use `think-tank` when the task needs:

- research from multiple sources
- review with explicit gaps and risks
- strategy tradeoffs
- council-style disagreement
- capability routing with provider boundaries

Do not use it for simple factual answers or one-step commands.

## Mode Selection

Use these defaults:

- `research`: gather evidence and compare options
- `review`: inspect artifacts and identify readiness gaps
- `council`: contrast viewpoints and surface disagreement
- `strategy`: prioritize paths and recommend direction

## Host Enhancement Paths

When `think-tank` is enhancing a host agent such as Codex, three paths are
especially valuable after the base modes are working:

- `research -> action`
  Use when evidence is already collected and the host agent now needs next
  steps, prioritization, and observation boundaries.
- `review -> readiness`
  Use when the host agent needs to know whether something is truly ready,
  partially ready, or blocked, and who should act next.
- `strategy -> backlog`
  Use when the host agent needs backlog candidates with readiness,
  dependencies, validation plan, and next owner.

These paths should produce host-consumable structure, not just good prose.

## Policy And Triggers

`think-tank` does not own built-in trigger words.

Trigger words, aliases, and provider preferences belong to user-owned YAML
policy. The public core provides:

- intent categories
- policy schema
- routing contracts
- example trigger classes

## Capability Routing

Think in slots, not tool names:

- `source-acquisition`
- `browser-automation`
- `social-listening`
- `knowledge-persistence`
- `media-processing`
- `media-production`

Choose a capability slot first. Choose a provider only after the task needs it,
the platform exposes it, the permission boundary is acceptable, and the
dispatch decision is explicit.

## Evidence Boundaries

Keep these states distinct:

```yaml
selected:
dispatched:
invoked:
recovered:
verified_partial:
verified:
```

The user should always be able to tell what really happened.
