# Project Leader Production Runbook (Execution)

Use this file for one-shot weekly execution and record.

## 1) Weekly run command

```bash
python3 leader-runtime/runtime/project_leader_ops.py \
  leader-runtime/examples/project-leader-pilot.sample.yaml \
  --log-csv leader-runtime/examples/project-leader-weekly-observations.csv \
  --operator leader \
  --host-provider codex-host-adapter \
  --notes "week_1_canary"
```

If you do not have host evidence for this run, add `--notes` only and keep
`candidate_host_results` in the pilot spec empty. This still records the
pre-invocation boundary behavior.

## 2) CSV tracking template

Copy template:

- [project-leader-weekly-observations-template.csv](../examples/project-leader-weekly-observations-template.csv)

Append rows to:

- `leader-runtime/examples/project-leader-weekly-observations.csv`

## 3) Minimal weekly decision checks

- `dispatch_status` should match expected `blocked` or `ready_for_host_dispatch`.
- `boundary_violations` should be `0` when evidence rules are met.
- `failed_invocations` should trend down after host adapter stabilization.
- If boundary violation appears, only continue after root cause is recorded in notes.
