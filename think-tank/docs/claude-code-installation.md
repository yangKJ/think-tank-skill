# Claude Code Installation Guide

This guide explains the public skill installation path for `think-tank` in Claude Code.

## Install As A Claude Code Skill

Install the generated skill bundle into one of these locations:

- User-wide: `~/.claude/skills/think-tank/`
- Project-local: `.claude/skills/think-tank/`

Generated artifact:

```text
dist/claude-code-skill/think-tank/
```

After copying the folder, restart Claude Code or start a new session.

## Packaging

Generate the Claude artifact with:

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
Use think-tank to review these notes, separate facts from assumptions, and give me a boundary-aware recommendation.
```

## Distribution Status

- Claude Code skill bundle distribution: ready
- Public self-serve Claude marketplace submission flow: not documented in the official sources used for this repository

That last point matters: if Anthropic later exposes a public listing flow, these artifacts are designed to be upload-ready, but today the safe public path is GitHub distribution plus direct skill install.
