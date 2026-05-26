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

## Step Map

复杂任务应在进入长流程执行前或执行中生成 step map。step map 用于把任务拆成可审计节点，而不是把一次长输出说成“全链路完成”。

```yaml
step_map:
  verification_status: step_map_built | step_map_partial | not_applicable
  provider_invoked: false
  public_or_destructive_action_included: false
  step_count: 0
  ready_step_count: 0
  blocked_step_count: 0
  steps:
    - step_id:
      title:
      stage:
      status: missing | partial | ready | running | completed | failed | blocked | skipped
      depends_on: []
      parallel_group:
      required_artifacts:
        - path_or_ref:
          exists: true | false | unknown
          verification_status: verified | verified_partial | unverified | missing | not_applicable
      recommended_action:
      boundaries: []
```

规则：

- `ready` 只表示该节点需要的输入或产物已具备，不代表后续节点已经执行。
- `completed` 必须有产物、结果或检查证据；不能只靠命令存在或计划存在。
- `provider_invoked: false` 的 step map 只能证明本地规划或审计，不证明外部 provider 已执行。
- 写入、发布、付费、登录态或破坏性动作必须在 step 上显式标注，并走 dispatch policy。

## Dependency Graph

长流程可以把 step map 降解成依赖图和批次，帮助平台判断哪些节点可以并行，哪些必须串行。

```yaml
dependency_graph:
  verification_status: dependency_graph_built | dependency_graph_partial | not_applicable
  nodes:
    - step_id:
      status:
  edges:
    - from:
      to:
  execution_batches:
    - batch_id:
      step_ids: []
      parallelizable: true | false
      status: ready | blocked | dependency_cycle_or_missing
```

如果出现依赖环、缺失依赖或未知状态，必须把批次标记为 `blocked` 或 `dependency_cycle_or_missing`，不能继续声明自动执行可行。

## Step Recovery Plan

当 step map 中存在 `missing`、`partial`、`failed` 或 `blocked` 节点时，应生成恢复计划。

```yaml
step_recovery_plan:
  verification_status: recovery_plan_built | recovery_plan_partial | not_applicable
  provider_invoked: false
  action_count: 0
  recovery_actions:
    - step_id:
      status:
      missing_artifacts: []
      recommended_action:
      requires_user_confirmation: true | false
      external_or_costly: true | false
      recovery_boundary:
```

恢复计划可以包含命令预览或人工动作建议，但它本身不等于执行。只有恢复动作真实运行并完成 result recovery 后，才能升级对应 step 状态。

## Human Runbook

对需要人工验收、跨工具交接或后续 agent 继续执行的任务，应输出简短 runbook。

```yaml
human_runbook:
  scope:
  excludes: []
  ready_count:
  blocked_count:
  steps:
    - step_id:
      status:
      dependencies: []
      next_action:
      review_notes:
```

runbook 是交接和验收材料，不是质量通过证明。它必须和 step map、dependency graph、recovery plan 或 artifact quality gates 一起使用。

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

## Team Cleanup

当使用 multi-agent team 时，必须保证 team 清理：

```yaml
team_cleanup:
  required: true
  verification: check_team_directory_empty
  failure_action: |
    1. 尝试 TeamDelete 重试（等待 2s）
    2. 检测 config.json 中 tmuxPaneId 状态
    3. 如卡在 in-process，提示用户手动清理
    4. 记录 zombie team 到 artifact，供后续清理
  artifact:
    - team_residue_manifest: []
    - cleanup_instructions: ""
```

详细规范见 `protocol/shutdown-contract.md`。

## Verification Status

```yaml
state_result_contract_v0_2: specified
automatic_recovery: not_verified
structured_manual_recovery: verified_partial
```
