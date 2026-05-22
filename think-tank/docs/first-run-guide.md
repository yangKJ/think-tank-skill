# First Run Guide

![First run guide](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/first-run-guide-image2.png)

This guide is for a user who has already installed `think-tank` and wants the
shortest path to a real first success.

## Goal

A successful first run means:

- the runtime can read `SKILL.md`
- the user can trigger research, review, or strategy-style structure
- the output separates evidence, inference, risk, and boundary
- no optional provider is falsely described as already invoked

## Fastest Path

1. Confirm the entry file exists in your runtime skill directory.
2. Restart the runtime or current session.
3. Use a prompt that clearly needs review, research, or strategy behavior.
4. Check that the response uses boundary-aware structure rather than generic
   freeform text.

## Recommended First Prompt

```text
Use think-tank to review these notes, separate facts from assumptions, and give me a boundary-aware recommendation.
```

## What Good Output Looks Like

The first response should make these things visible:

- what the task is solving
- what is known versus inferred
- what the next recommendation is
- what is not verified

## What Usually Goes Wrong

- the runtime was not restarted after installation
- the prompt is too small, so the runtime answers directly
- the user expects optional providers to already be authorized
- the user treats documented patterns as proof of invocation

## First Success Boundary

Your first success does not need browser automation, social provider access,
media processing, private knowledge-base writes, or true multi-agent runtime.
It only needs a clear boundary-aware response from the public skill core.
