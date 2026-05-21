# Skill Trigger Intelligence

`skill-trigger-intelligence` defines how an agent decides whether to use
`think-tank` before loading deeper references or invoking optional providers.

It is a decision protocol, not a built-in trigger-word table.

## Core Rule

`think-tank` core must not own project-specific trigger words.

Trigger words, aliases, platform shortcuts, provider preferences, and local
workflow bindings belong in user-owned routing policy files such as:

```text
routing/policy-schema.md
platforms/<platform>/provider-policy.example.yaml
```

The public skill may document trigger categories and examples, but those
examples are not executable rules until a user's own YAML policy adopts them.

## Decision Goals

Before using `think-tank`, the agent should decide:

- whether the task benefits from multi-role reasoning
- whether evidence collection or provider routing is needed
- whether a lightweight direct answer is enough
- whether a platform adapter or optional peer skill is required
- which boundary must be disclosed before execution

## Positive Signals

Use `think-tank` when one or more of these are true:

- the task asks for research, competitive analysis, market analysis, technical
  evaluation, review, strategy, or council-style discussion
- the answer requires multiple roles, tradeoff analysis, disagreement, or risk
  review
- the task needs source acquisition, browser work, media processing, knowledge
  persistence, social listening, or other capability slots
- the output should include conclusion, evidence, disagreement, risk, and
  action recommendations
- the task is likely to become reusable as a run record, memory candidate,
  research artifact, or backlog candidate

## Negative Signals

Do not use `think-tank` when the user asks for:

- a simple factual answer
- a one-step command
- a narrow edit with no broader review
- a short translation or rewrite
- a task where no evidence, role split, or capability routing is useful

## Policy-Owned Trigger Examples

These examples are only suggested phrases for a user's YAML policy:

```yaml
trigger_examples:
  research:
    - "research this"
    - "deep research"
    - "competitive analysis"
  council:
    - "discuss this"
    - "decision council"
  review:
    - "review this"
    - "acceptance check"
  strategy:
    - "make a roadmap"
    - "strategy plan"
```

The skill itself must treat them as documentation examples, not as hard-coded
activation rules.

## Required Decision Block

When the task is ambiguous, produce a compact `skill_route_decision` before
loading deep references:

```yaml
skill_route_decision:
  user_goal:
  should_use_think_tank: true | false
  reason:
  selected_intent:
  selected_mode:
  needs_provider_routing: true | false
  policy_source: user_yaml | platform_default | protocol_default
  trigger_source: user_policy | inferred_intent | explicit_user_request | none
  confidence: high | medium | low
  boundary:
```

## Decision Outcomes

- `use_think_tank`: use the skill protocol.
- `use_lightweight_mode`: use only `SKILL.md` and one relevant mode/protocol
  reference.
- `do_not_use`: answer directly and disclose that the task does not need the
  skill.
- `request_policy_or_context`: ask for user policy or context when activation
  would be risky.
- `escalate_to_provider_pattern`: use `think-tank` plus routing docs because a
  capability slot may need an optional peer provider.

## Verification Boundary

Never claim a trigger is installed or active unless a platform or project YAML
policy actually defines it.

Acceptable wording:

```yaml
trigger_status: example_only
policy_loaded: false
activation_basis: inferred_intent
```

Unacceptable wording:

```yaml
trigger_status: built_in
activation_basis: hardcoded_keyword
```
