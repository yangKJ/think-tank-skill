# Project Leader Pilot Runbook

这份 runbook 说明其他 Codex 项目如何用 `leader-runtime/` 跑第一轮领导化试点。

## 为什么要先跑试点

领导化架构建好以后，最容易出现的误区有两个：

1. 只看 schema 和样例，以为项目已经真正进入多专家协作。
2. 直接接真实 host，却没有先把 selection、promotion、gate 和 evidence 边界验证清楚。

先跑试点的价值是：

- 用一轮最小项目流验证 leader 控制面是否闭环。
- 让项目 owner 看清楚哪些状态只是规划，哪些状态已经有 evidence。
- 给其他项目提供可复制的接入模板，而不是每次重新拼装流程。

## 试点输入

一个最小试点由一份 pilot spec 驱动：

```text
leader-runtime/examples/project-leader-pilot.sample.yaml
```

关键字段：

- `selection_policy`
- `request`
- `approved_agent_ids`
- `allow_candidate_invocation`
- `candidate_runtime_support`
- `candidate_host_results`

## 运行路径

```text
project leader pilot
  -> selection policy
  -> candidate review / promotion
  -> project team activation
  -> project-aware orchestrator
  -> invocation gate
  -> host-ready dispatch bundle
  -> host invocation evidence
```

运行入口：

```text
python3 leader-runtime/runtime/project_leader_pilot.py \
  leader-runtime/examples/project-leader-pilot.sample.yaml
```

## 验收重点

- `selection_result.selected_count` 是否合理
- `review_report.promoted_count` 是否符合审核预期
- `project_team_activation.candidate_agents` 是否只包含 promoted candidate
- `project_candidate_invocation_gate` 是否保持 gate 语义
- `project_candidate_host_dispatch_bundle.dispatch_status` 是否清楚区分 blocked 与 ready
- `project_candidate_invocation_evidence.results[].invoked` 是否只在 host 回灌后为 true

## 优点

- 把主 agent 的领导化落地成可重复运行的项目流程。
- 把 candidate、promotion、activation、dispatch、evidence 分层讲清楚。
- 方便未来不同项目替换自己的 selection policy 和专家队伍。

## 边界和缺点

- 试点默认只能证明仓库内控制面闭环，不自动证明外部 host 的长期稳定性。
- 样例 evidence 仍然可以是 repo 内样例文件，因此它更像验收底稿，不是生产观测。
- 真正的生产化还需要项目自己接入 host 侧真实调用和失败恢复。
