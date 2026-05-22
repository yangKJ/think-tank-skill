# Eval Contracts

Every eval case must include:

- `eval_id`
- `case_type`
- `fixture`
- `expected_contracts`
- `actual_contracts`
- `passed`
- `failures`
- `residual_risk`

Eval fixtures must not claim provider invocation, true multi-agent runtime, private writes, or factual correctness unless the fixture contains evidence for that claim.
