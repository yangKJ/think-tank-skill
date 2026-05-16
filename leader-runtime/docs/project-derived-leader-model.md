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
```
