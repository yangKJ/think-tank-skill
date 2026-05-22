# Strategy To Backlog

`strategy_to_backlog` 把 think-tank 的策略结论转成可执行候选任务。它不是自动排期，也不是直接修改项目代码；它是从调研到执行的中间契约。

## Goal

```yaml
feature: strategy_to_backlog
scope: strategy_research_review_outputs
purpose: convert_recommendations_to_actionable_work
```

## Required Structure

```yaml
strategy_to_backlog:
  backlog_candidates:
    - title: "<task title>"
      readiness: ready | needs_input | observe_only | blocked
      priority: P0 | P1 | P2
      reason: "<why this matters>"
      affected_area:
        - "<module, product area, docs, runtime, platform>"
      evidence:
        - "<source id or claim>"
      acceptance_criteria:
        - "<observable pass condition>"
      non_goals:
        - "<what this task must not include>"
      dependencies:
        - "<optional dependency>"
      risk:
        - "<main risk>"
      next_owner: "<who should pick this up next>"
  sequencing:
    - "<recommended order>"
  validation_plan:
    - "<how to verify the backlog item>"
```

## Priority Semantics

- `P0`：定位、闭环、质量门禁或用户价值核心阻塞。
- `P1`：显著提升产品、runtime 或复用能力，但不阻塞当前可用性。
- `P2`：增强项、规模化项、长期护城河或后续探索。

## Rules

- 每个 backlog 候选必须有验收标准。
- 每个 backlog 候选必须有非目标，防止策略建议膨胀成无边界任务。
- 证据不足的建议必须降低优先级或标注风险。
- `observe_only` 表示值得持续跟踪，但当前不建议执行。
- `blocked` 表示方向成立，但缺关键依赖或输入，不能直接进入执行。
- 每个候选都应明确 `next_owner`，避免“看起来合理，但没人接”。
- 不得把 strategy_to_backlog 写成承诺已实现。

## Quality Gates

```yaml
recommendations_have_acceptance_criteria: true
non_goals_present: true
priority_reasonable: true
validation_plan_present: true
not_claimed_as_implemented: true
```
