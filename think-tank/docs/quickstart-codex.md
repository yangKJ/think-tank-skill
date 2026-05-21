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
think-tank/examples/public/research-request.md
think-tank/examples/public/council-decision.md
think-tank/examples/public/review-acceptance.md
```

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
