# Claude Code Runtime Pipeline v0.2

本文定义 Claude Code adapter 如何映射 v0.2 runtime library。

## Pipeline

```text
planner.plan_runtime
  -> slot_resolver.resolve_slots
  -> WebFetch invocation
  -> state_model.StageResult
  -> consensus.evaluate_consensus
  -> runtime_result
```

## Mapping

```yaml
runtime: claude-code-runtime-pipeline
planner:
  source: runtime/planner.py
slot_resolution:
  source: runtime/slot_resolver.py
  source-acquisition:
    candidates:
      - WebFetch
      - web-access
state_result:
  source: runtime/state_model.py
invocation:
  method: WebFetch
  target_scope:
    - public_static_web
consensus:
  source: runtime/consensus.py
```

## Required Output

Claude Code pipeline 必须输出同一份平台无关结构：

```yaml
runtime_result:
  runtime: claude-code-runtime-pipeline
  mode: research
  runtime_plan: {}
  slot_resolution: {}
  run_state: {}
  source_result: {}
  consensus_result: {}
  final_output: {}
  quality_check: {}
  boundaries: []
```

## Status

```yaml
claude_code_runtime_pipeline_spec: specified
claude_code_runtime_pipeline_execution: planned
adapter_dispatch_runtime: not_full_verified
automatic_recovery: not_verified
```

## 不得声明

- 不得把 WebFetch 单次调用称为完整 adapter runtime。
- 不得把 structured manual recovery 称为 automatic recovery。
- 不得把本规范当成 Claude Code Team 真并发证明。
