# Platform Publishing Guide

This document explains what can be published today, what can only be prepared, and which artifacts in this repository are intended for each platform.

## Current Reality

As of 2026-05-21:

- OpenAI documents workspace skill creation, upload, install, and sharing inside ChatGPT Skills.
- OpenAI states that skills are also supported in Codex, but public cross-product sync is not available yet.
- Claude Code skill distribution should target the `.claude/skills/` directory.
- Anthropic mentions a skills ecosystem and partner directory, but a public self-serve submission flow for an open Claude skill directory was not documented in the sources used for this repo.

## OpenAI / ChatGPT Skills / Codex

Recommended artifact:

```text
dist/openai-chatgpt-skill/think-tank/
```

Metadata:

```text
marketplace/openai-skill-listing.yaml
```

Recommended publish path:

1. Generate artifacts with `python3 scripts/package_agent_distributions.py`.
2. Open ChatGPT Skills.
3. Upload the `dist/openai-chatgpt-skill/think-tank/` bundle.
4. Validate starter prompts.
5. Share to your workspace or publish to your workspace library.

Current status:

- workspace publish readiness: ready
- public Codex skill store submission flow: not documented

## Claude Code / Claude Skills Ecosystem

Recommended artifacts:

```text
dist/claude-code-skill/think-tank/
```

Metadata:

```text
marketplace/claude-skill-listing.yaml
```

Recommended publish path today:

1. Generate artifacts with `python3 scripts/package_agent_distributions.py`.
2. Distribute via GitHub release or direct download.
3. Install the skill bundle into `~/.claude/skills/think-tank/` or `.claude/skills/think-tank/`.

Current status:

- GitHub distribution readiness: ready
- Claude Code skill install path: ready
- public self-serve directory submission flow: not documented

## Why This Repository Uses Multiple Artifacts

The public skill core is the portable source of truth:

```text
think-tank/
```

But platforms differ in how they discover and load agent behaviors:

- OpenAI Skills accept Agent Skills-style bundles.
- Claude Code skill distribution should use the `.claude/skills/` directory.
- Future marketplace or directory flows may ask for metadata, starter prompts, or upload-ready zips.

This repo therefore keeps:

- one reusable skill core
- one packaging script
- one listing metadata set per platform
