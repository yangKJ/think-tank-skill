# Progressive Disclosure

`think-tank` should be easy for agents to load without pulling the whole
repository into context.

This protocol defines the recommended loading order.

## Principle

Load only the smallest reference set needed to make the next correct decision.

Do not load all profiles, all recipes, all examples, all platform adapters, or
all provider docs unless the task explicitly needs them.

## Loading Order

### 1. Entrypoint

Always start with:

```text
SKILL.md
```

Use it to decide whether the task is in scope and which mode is likely.

### 2. Trigger And Invocation

For ambiguous activation or non-trivial work, load:

```text
protocol/skill-trigger-intelligence.md
protocol/skill-invocation-contract.md
```

### 3. Mode And Intent

Load only the mode and intent files required by the task:

```text
protocol/intent-routing.md
protocol/mode-selection.md
modes/<selected-mode>.md
```

### 4. Recipe

Load a recipe only after the selected intent implies a reusable workflow:

```text
recipes/<selected-recipe>.md
```

### 5. Profiles

Load only profiles that will participate in the work:

```text
profiles/<selected-profile>.md
```

Do not load every profile to simulate breadth.

### 6. Capability And Provider Routing

Load capability and routing docs only when a task needs optional tools:

```text
capabilities/<capability>.md
routing/skill-router.md
routing/dispatch-policy.md
routing/result-recovery.md
```

Then load one platform adapter if needed:

```text
platforms/<platform>/README.md
```

### 7. Runtime, Memory, And Research OS

Load these only when the task needs persistent records, handoff, replay, or
workspace organization:

```text
protocol/run-record.md
protocol/project-memory-runtime.md
protocol/research-os.md
protocol/handoff-protocol.md
protocol/provider-invocation-ledger.md
```

### 8. Examples And Self Tests

Load examples only to clarify expected structure:

```text
examples/public/
examples/v3/
self-tests/
```

## Disclosure Plan

For complex work, emit:

```yaml
progressive_disclosure_plan:
  initial_refs:
  conditional_refs:
  skipped_refs:
  reason:
  max_context_boundary:
```

## Anti-Patterns

- loading all docs before deciding mode
- treating example trigger phrases as installed triggers
- reading every provider pattern before confirming provider need
- loading platform docs for platforms that are not in use
- loading memory/runtime docs when the user only asked for a short answer

## Success Criteria

A compliant agent can explain:

- why `think-tank` was or was not used
- which refs were loaded
- which refs were intentionally skipped
- whether any provider was selected, invoked, or only documented
- what boundary remains unverified
