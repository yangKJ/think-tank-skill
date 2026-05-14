# Project Memory Capture

Use this recipe when the user asks to remember, preserve, or convert a
think-tank result into project-local knowledge.

## Triggers

```text
用 think-tank 生成项目记忆候选
用 think-tank 把这次分析沉淀成项目记忆候选
think-tank memory candidate
think-tank 项目记忆
把这次分析变成 think-tank 项目记忆候选
```

Avoid generic memory triggers such as `记下来` in public default policy. That
phrase may belong to the host platform's own memory system or a user's personal
workflow. Project-local policy may opt into shorter triggers only when the user
explicitly wants them.

## Default Mode

```yaml
mode: review
profiles:
  - skeptic
  - report-architect
capabilities:
  - knowledge-persistence
default_behavior: propose_only
write_requires_confirmation: true
```

## Flow

1. Extract memory candidates from the current run.
2. Classify each candidate as architecture, workflow, convention, pitfall, or
   decision.
3. Attach source evidence and verification date.
4. Label scope, privacy, status, confidence, staleness risk, and expiry rules.
5. Check for duplicates in the chosen target.
6. Propose a patch or structured write.
7. Write only after explicit user confirmation or an explicit direct-write
   instruction.
8. Report written and skipped items.

## Target Preference

```yaml
preferred_targets:
  - .think-tank/memory/
  - AGENTS.md
fallback_target: propose_only
forbidden_default_targets:
  - think-tank/
```

## Quality Rules

- If source evidence is missing, do not write as a fact.
- If privacy is `private`, do not write to tracked public docs.
- If a target is inside `think-tank/`, reject by default.
- If the item repeats existing memory, skip or merge instead of duplicating.
- If the item depends on current tool availability, mark staleness risk and
  require a refresh trigger before using it as current fact.
- If the item has no `expires_when`, do not write it.

## Minimal Output

```yaml
selected_recipe: project-memory-capture
memory_candidates:
  - type: workflow
    title: Provider selection is not provider invocation
    target: .think-tank/memory/workflows.md
    action: append
    privacy: project_local
    status: active
    staleness_risk: low
    expires_when: user changes project policy
    review_after: null
    refresh_trigger:
      - before changing provider policy semantics
    confidence: high
quality_check:
  has_source: true
  has_scope: true
  has_expiry_rule: true
  no_secret: true
  write_requires_confirmation: true
boundaries:
  - This recipe proposes local memory; it does not alter public Skill protocol.
```
