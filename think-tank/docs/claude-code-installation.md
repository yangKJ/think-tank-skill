# Claude Code Installation Guide

This guide explains the two realistic distribution paths for `think-tank` in Claude Code today.

## Path 1: Install As A Claude Code Subagent

This is the clearest documented Claude Code path in Anthropic's public docs.

Install the generated subagent file into one of these locations:

- User-wide: `~/.claude/agents/think-tank.md`
- Project-local: `.claude/agents/think-tank.md`

Generated artifact:

```text
dist/claude-code-subagent/think-tank.md
```

After copying the file, restart Claude Code or start a new session.

## Path 2: Install The Agent Skills Core Bundle

If your Claude-side environment supports Agent Skills directly, use the generated skill core bundle:

```text
dist/claude-code-skill/think-tank/
```

This path is useful for teams that want the portable `SKILL.md` + resources bundle instead of only a Claude-specific subagent wrapper.

## Packaging

Generate both Claude artifacts with:

```bash
python3 scripts/package_agent_distributions.py
```

## First-Install Validation

1. Confirm the expected file exists.
2. Restart Claude Code or start a fresh session.
3. Send a small prompt that should trigger research, review, council, or strategy behavior.
4. Check that the output distinguishes evidence from assumptions and does not overclaim runtime capabilities.

Suggested first prompt:

```text
Use the think-tank subagent to review these notes, separate facts from assumptions, and give me a boundary-aware recommendation.
```

## Distribution Status

- Claude Code subagent distribution: ready
- Agent Skills core bundle for Claude-side reuse: ready
- Public self-serve Claude marketplace submission flow: not documented in the official sources used for this repository

That last point matters: if Anthropic later exposes a public listing flow, these artifacts are designed to be upload-ready, but today the safe public path is GitHub distribution plus direct install.
