# Evidence Recovery Contract

本文定义 think-tank 在证据不足、验收不扎实、provider 仅部分成功或结果仍需升级时的统一恢复契约。

它解决的问题不是“当前证据够不够”，而是：

> 如果当前证据还不够，接下来缺什么、谁去补、怎么补、补完后预期把状态升级到哪里。

## 目的

```yaml
feature: evidence_recovery_contract
scope: platform_neutral
purpose: turn weak evidence into actionable recovery steps
```

## 适用场景

在以下任一情况，应输出 `evidence_recovery_plan`：

- `evidence_state` 为 `selected`、`dispatched`、`invoked`、`recovered` 或 `verified_partial`
- `acceptance_ready` 已给出，但证据质量仍偏弱
- provider 调用有结果，但 recovery 或 verification 仍不完整
- 当前结论可作为阶段性判断，但不适合长期沉淀或高风险采纳

## 核心原则

- 保持平台无关
- 保持项目无关
- 区分“谁补证据”与“谁做最终决定”
- 区分“必须真实调用 provider”与“宿主本地即可补齐”
- 不把 recovery plan 伪装成已完成执行

## 最小结构

```yaml
evidence_recovery_plan:
  target_question:
  current_evidence_state:
  confidence: low | medium | high
  blocking_gap:
  target_upgrade_state:
  recovery_actions:
    - action_id:
      actor: host_agent | provider | human
      action:
      invocation_required: true | false
      expected_artifacts: []
      success_condition:
      failure_behavior:
  fallback_if_unavailable:
  boundaries: []
```

## 字段说明

### `target_question`

- 当前 recovery plan 在试图补强哪个结论或验收点

### `current_evidence_state`

- 使用统一状态词：
  - `selected`
  - `dispatched`
  - `invoked`
  - `recovered`
  - `verified_partial`
  - `blocked`
  - `failed`

### `confidence`

- 当前在未补强前，对阶段性结论的把握度

### `blocking_gap`

- 用一句话说明当前最关键的证据缺口
- 不能只写“证据不足”

### `target_upgrade_state`

- 说明 recovery 成功后，期望把状态提升到哪里
- 通常是：
  - `recovered -> verified_partial`
  - `verified_partial -> verified`

### `recovery_actions`

每个 action 必须说明：

- `actor`
  - `host_agent`：宿主 agent 本地可补
  - `provider`：需要真实 provider / tool / worker 调用
  - `human`：必须用户或人工确认
- `action`
  - 具体动作
- `invocation_required`
  - 是否要求真实外部调用
- `expected_artifacts`
  - 补完后应出现的证据或产物
- `success_condition`
  - 什么叫补成功
- `failure_behavior`
  - 补不出来时如何降级

### `fallback_if_unavailable`

- 如果关键 provider、权限、环境不可用，当前 plan 应如何保守降级

### `boundaries`

- 当前 recovery plan 未覆盖的边界

## 使用规则

### 1. recovery plan 不是执行证明

输出了 `evidence_recovery_plan`，不代表 recovery 已执行完成。

### 2. 必须与当前结论关联

recovery plan 必须服务于一个明确的结论、验收判断或任务包边界，不能脱离当前问题孤立存在。

### 3. action 必须可执行

不要写成抽象建议；必须能让后续执行者知道：

- 去查什么
- 去跑什么
- 去补什么 artifact

### 4. 优先补“最小关键缺口”

如果缺口很多，优先列出最小、最关键、最能升级结论可信度的动作，不要求一次列完所有潜在补证据项。

## 推荐升级路径

```yaml
upgrade_examples:
  recovered_to_verified_partial:
    common_gap: "已有结果，但缺验证证据或作用范围说明"
  verified_partial_to_verified:
    common_gap: "已有真实路径，但缺可重复 procedure 或质量门禁证据"
  blocked_to_verified_partial:
    common_gap: "当前环境不可用，需要替代 provider 或人工补证"
```

## 最小质量门禁

```yaml
evidence_recovery_quality_check:
  target_question_explicit: true
  blocking_gap_specific: true
  target_upgrade_state_explicit: true
  action_owner_explicit: true
  invocation_boundary_clear: true
  success_condition_present: true
  fallback_present: true
```

## Verification Status

```yaml
evidence_recovery_contract_v0_1: specified
project_binding: none
provider_binding: none
intended_use:
  - worker_acceptance_follow_up
  - decision_follow_up
  - provider_result_upgrade
  - evidence_gap_recovery
```
