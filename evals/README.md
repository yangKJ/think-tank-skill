# Eval Pack Starter

`evals/` contains lightweight regression fixtures for public protocol behavior.

The eval pack checks structure and boundary discipline. It does not prove factual correctness for arbitrary real-world claims.

## Case Types

- research output shape
- provider selected-not-invoked fallback
- memory promotion decision
- handoff guardrail
- open-source readiness review

## Layout

```text
evals/
├── cases/
├── fixtures/
└── expected/
```

## Rule

Every eval case should declare:

```yaml
eval_id:
case_type:
fixture:
expected_contracts: []
actual_contracts: []
passed:
failures: []
residual_risk: []
```
