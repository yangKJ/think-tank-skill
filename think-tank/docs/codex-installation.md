# Codex Installation Guide

This guide explains how to use `think-tank` from Codex without bundling private local configuration.

## Option 1: Use This Repository Directly

Clone the repository and reference the skill directory:

```text
think-tank/
```

This is useful when you want to read docs, run checks, or contribute changes.

## Option 2: Copy The Skill Core

Copy only the public skill core into your Codex skills directory:

```text
think-tank/
```

Do not copy local runtime folders such as:

```text
.codex/
.think-tank/
.claude/
outputs/
checks/__pycache__/
```

## What Is Included

```yaml
included:
  - think-tank/SKILL.md
  - think-tank/protocol/
  - think-tank/capabilities/
  - think-tank/profiles/
  - think-tank/platforms/
  - think-tank/modes/
  - think-tank/recipes/
  - think-tank/routing/
  - think-tank/templates/
  - think-tank/schemas/
  - think-tank/examples/
  - think-tank/docs/
```

## What Is Not Included

```yaml
not_included:
  - peer skill installations
  - user API keys
  - provider login state
  - local provider policy
  - private project memory
  - generated outputs
```

Peer skills are user-installed and user-authorized. A provider being mentioned in docs means `pattern_documented`, not `invoked`.

## Minimal Validation

From the repository root:

```bash
python3 checks/open_source_release_suite.py
python3 checks/stable_release_check.py
```

If you copied only `think-tank/` into another environment, use the docs and examples as protocol references. The repository-level checks require this full repository layout.
