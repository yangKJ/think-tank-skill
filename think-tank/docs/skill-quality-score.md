# Skill Quality Score

The Skill Quality Score is a lightweight rubric for evaluating whether
`think-tank` is easy and safe for agents to use.

It does not score model intelligence. It scores skill packaging, invocation
clarity, boundaries, examples, and regression coverage.

## Rubric

| area | max | expectation |
|---|---:|---|
| Trigger clarity | 10 | clear positive and negative use signals; no hard-coded public trigger words |
| Invocation contract | 10 | agent can form input and output contracts before deep execution |
| Progressive disclosure | 10 | docs are loadable in small, task-specific chunks |
| Mode and recipe routing | 10 | research, council, review, and strategy are easy to select |
| Provider boundaries | 10 | selection, preflight, invocation, recovery, and verification are distinct |
| Agent compatibility | 10 | Codex, Claude Code, and generic fallback behavior are documented |
| Examples | 10 | examples cover decisions, contracts, disclosure, and self-test results |
| Self tests | 10 | fixtures catch trigger, anti-trigger, provider, composition, and memory cases |
| Privacy and release boundary | 10 | public core excludes local state, secrets, private projects, and generated runs |
| Documentation navigation | 10 | README, docs index, protocol index, and examples index point to the right files |

## Score Bands

| score | meaning |
|---:|---|
| 90-100 | stable skill experience |
| 75-89 | usable with documented gaps |
| 60-74 | beta; needs clearer docs or tests |
| below 60 | not ready for public agent use |

## Current Target

```yaml
target_release: v3.0
target_band: stable skill experience
minimum_score: 90
required_gate: checks/skill_experience_check.py
```

## Required Evidence

A score should cite:

- protocol files used for trigger, invocation, and disclosure
- examples proving expected machine-readable structure
- self-test fixtures proving common boundaries
- release checks proving the files remain present and linked

## Boundary

This rubric does not mean every optional provider works. It means the skill tells
agents how to decide, disclose, invoke, degrade, and verify.
