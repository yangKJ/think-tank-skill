# Codex Quickstart

This guide summarizes the shortest Codex path.

## 1. Install Or Reference The Skill

Use the public Skill core:

```text
think-tank/
```

Do not copy private runtime state, generated outputs, provider login state, or local workspace data.

## 2. Start With Public Examples

```text
think-tank/examples/usage/research-request.md  
think-tank/examples/usage/council-decision.md
think-tank/examples/usage/review-acceptance.md  
think-tank/examples/usage/research-to-action.md  
think-tank/examples/usage/strategy-backlog.md  
```

If your goal is to improve the host agent rather than just collect evidence,
start with:

- `research-to-action` when you need next steps, prioritization, or observation boundaries
- `review-acceptance` when you need readiness, blocker classification, or next owner
- `strategy-backlog` when you need backlog candidates with readiness and ownership

## 3. Run Validation

```bash
python3 checks/open_source_release_suite.py
python3 checks/stable_release_check.py
```

## 4. Add Optional Providers Carefully

Provider examples are patterns. Before reporting a provider as working, record:

```yaml
route_selected:
provider_preflight:
dispatch_decision:
invoked_providers:
not_invoked_providers:
recovery:
verification_status:
```

## 5. Use 2.0 Contracts

For long-running work, use:

- run records
- provider invocation ledgers
- memory runtime results
- handoff packets
- guardrail results
- eval fixtures
