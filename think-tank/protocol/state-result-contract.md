# State And Result Contract

本文定义 think-tank v0.2 的 state/result 最小契约。

它吸收旧 research think-tank `core/state.py` 的经验，但不要求所有平台都使用文件系统状态。

## 目的

state/result contract 用于保证长流程可恢复、可审计、可标注边界。

## Run Identity

```yaml
run:
  run_id: string
  protocol_version: string
  mode: research | council | review | strategy
  status: pending | running | completed | failed | timed_out | cancelled
  created_at: timestamp
  started_at: timestamp | null
  completed_at: timestamp | null
```

要求：

- `run_id` 必须可追踪。
- `run_id` 不得包含路径穿越字符。
- 平台可以使用 UUID、时间戳或会话 id。

## State

```yaml
state:
  current_stage: intake | collection | analysis | deliberation | synthesis | recommendation | quality_check
  current_round: integer
  selected_profiles: []
  selected_capabilities: []
  completed_stages: []
  pending_stages: []
  boundaries: []
```

## Heartbeat

heartbeat 是平台可选能力，不是 core 必需能力。

```yaml
heartbeat:
  actor: ""
  status: alive | working | completed | failed
  current_action: ""
  last_seen_at: timestamp
```

## Result

每个 profile 或 stage 的结果至少包含：

```yaml
result:
  actor: ""
  stage: ""
  claim: ""
  evidence: []
  risks: []
  disagreements: []
  recommendations: []
  confidence: low | medium | high
  boundaries: []
```

## Recovery

```yaml
recovery:
  result_recovered: true | false
  recovered_as:
    - sources[]
    - evidence[]
    - role_views[]
  recovery_method: automatic | structured_manual | unavailable
  recovery_boundary: ""
```

规则：

- `structured_manual` 可以作为 partial 状态。
- 只有平台有可重复自动过程时，才能标记 `automatic`。
- 未回收结果不得伪造成已验证 evidence。

## Persistence

平台可以选择：

- repository artifact
- `.think-tank/runs/<run_id>/`
- memory connector
- external knowledge base

但 persistence 是 adapter 实现，不是协议硬依赖。

## Verification Status

```yaml
state_result_contract_v0_2: specified
automatic_recovery: not_verified
structured_manual_recovery: verified_partial
```
