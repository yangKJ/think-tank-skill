# Project Derived Leader Model

本文定义其他 Codex 项目如何从 `leader-runtime/` 派生自己的主 agent 领导者。

目标不是让每个项目重新发明一套领导机制，而是：

- 继承母体领导者规则
- 裁剪专家编制
- 叠加项目约束
- 保持统一的派遣与验收契约

## 派生关系

```text
leader-runtime global leader
  -> project leader
  -> project team pack
  -> project acceptance overrides
```

## Project Leader

项目领导者是主 agent 的项目级身份定义。

它至少应回答：

- 这个项目是谁的派生 leader
- 它默认可以调用哪些专家
- 它默认适用哪些 mode
- 它是否限制某些能力或派遣路径
- 它的验收覆盖规则是什么

## Project Team Pack

项目专家编制是从全量专家池裁剪出来的项目可用专家子集。

它至少应回答：

- 继承哪个全量 registry
- 明确启用哪些专家
- 明确禁用哪些专家
- 是否需要追加项目标签
- 是否需要追加能力偏好

## 设计原则

1. 项目派生只做裁剪和覆盖，不重写母体领导者协议。
2. 项目可以减少专家，但不应擅自改变专家语义。
3. 项目可以新增约束，但不应把 `planned` 写成 `verified`。
4. 项目级覆盖必须可回溯到母体 leader 与 team pack。

## 最小派生流程

```text
global leader
  -> choose project team pack
  -> derive project registry
  -> create project leader identity
  -> run project-specific dispatch and acceptance
```

## Project-aware Orchestrator

项目 team pack 通过 review 和 activation 后，可以传给 Codex leader orchestrator：

```text
leader-runtime/runtime/orchestrator.py \
  "任务描述" \
  --team-pack leader-runtime/examples/promoted-project-team-pack.sample.yaml
```

输出中会出现：

```yaml
leader_context:
  project_team:
    project_id:
    pack_id:
    active_count:
project_team_activation:
  dispatch_roster:
    - source: global_registry
    - source: project_candidate
project_candidate_task_packets:
  - dispatch_status: planned_uninvoked
project_candidate_invocation_gate:
  decision_status: blocked | ready_uninvoked
  candidate_decisions:
    - invoked: false
project_candidate_host_dispatch_bundle:
  dispatch_status: blocked | ready_for_host_dispatch
project_candidate_invocation_evidence:
  results:
    - invoked: true
```

边界：

- project-aware orchestrator 只加载 roster，不调用 candidate subagent。
- `promoted_uninvoked` 不是 `invoked`。
- `planned_uninvoked` 只是派遣计划，不是执行证据。
- `ready_uninvoked` 只是允许进入下一层 adapter，不是执行证据。
- `ready_for_host_dispatch` 只是 adapter-ready，不是执行证据。
- 只有 host 回灌的 `invoked: true` evidence 才能证明真实调用发生。
- 项目队伍不修改 `global-experts.yaml`。

## 输出对象

第二阶段最小派生实现应至少生成：

- `project_leader`
- `project_team_pack`
- `derived_project_registry`
- `project_acceptance_profile`

## 当前状态

```yaml
project_derived_leader_model: implemented_partial
project_team_pack_schema: specified
derived_registry_runtime_helper: implemented
project_acceptance_override: specified
project_leader_pilot_flow: implemented
```

## 项目试点闭环

当前仓库已经内置一条最小试点闭环：

```text
leader-runtime/runtime/project_leader_pilot.py \
  leader-runtime/examples/project-leader-pilot.sample.yaml
```

这条命令会把一次项目 leader 演练串成单个输出对象，覆盖：

- candidate selection
- candidate review / promotion
- project team activation
- orchestrator dispatch
- invocation gate
- host-ready dispatch bundle
- host invocation evidence

它适合作为其他 Codex 项目的第一轮验收底稿。边界仍然不变：样例里使用的 host evidence 是 repo 内样例文件，因此它证明的是控制面闭环，而不是所有外部 host 的长期真实可用性。

生产环境放量建议参照：

- [project-leader-production-operations.md](project-leader-production-operations.md)
