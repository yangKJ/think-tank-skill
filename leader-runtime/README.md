# leader-runtime

`leader-runtime/` 是本仓库中与 `think-tank/` 同级的主 agent 领导者运行层。

它不是一个高阶 Skill，也不是某个平台的零散脚本集合。

它负责定义：

- 主 agent 的领导者身份
- 全量专家池 registry 与项目裁剪专家池
- dispatch decision
- expert task packet
- acceptance governance
- 项目级 leader 派生方式

## 与 think-tank 的关系

`think-tank/` 仍然是跨平台、可复用的高阶 Skill core。

`leader-runtime/` 则是更高一层的组织运行层。

关系应当是：

```text
leader-runtime
  -> 组织主 agent 身份、专家编制、派遣与验收
  -> 调用 think-tank 作为研究 / 审议 / review / strategy 技能
```

而不是：

```text
think-tank
  -> 反过来定义整个主 agent 的领导者系统
```

## 目录结构

```text
leader-runtime/
├── README.md
├── docs/
├── project-templates/
├── registries/
├── runtime/
├── schemas/
└── templates/
```

## Expert Registry

全局专家池的当前数据源是：

```text
registries/global-experts.yaml
```

`runtime/leader_registry.py` 读取这份 registry 后生成运行时 payload、候选专家摘要、dispatch decision 和 expert task packet。这样主 leader 的专家组织不再硬编码在 Python 里，后续可以按项目派生 team pack，也可以逐步把更多专家迁入统一 registry。

硬边界：

- registry 命中不等于 expert invocation。
- `availability_status` 只表达该专家定义或局部验证状态，不代表所有任务端到端可用。
- 项目级 team pack 可以裁剪专家池，但不能改写全局专家语义。

## Frontmatter Sources

Claude Code 的本地 subagent 文件通常用 frontmatter 表达基础身份：

```yaml
name:
description:
color:
emoji:
vibe:
tools:
```

这些字段非常适合作为 `leader-runtime` 的专家候选输入源。当前桥接入口是：

```text
runtime/agent_frontmatter.py
```

它只做三件事：

- 读取本地 `.claude/agents/**/*.md` 或样例文件的 frontmatter。
- 生成 `source-agent-frontmatter` candidate。
- 给出 domain、tools 和 authority scope 的初步 hint。

它不会直接把 Claude agent 注册进 `global-experts.yaml`，也不会声明这些 agent 已在 Codex 中被真实调用。candidate 进入 registry 前必须经过 leader 审核、去私有化、去平台绑定和验收边界补齐。

## Candidate Selection Policy

不同项目可以使用不同的 subagent 队伍。`leader-runtime` 因此不把本地 `.claude/agents` 固化为全局专家池，而是提供项目级筛选策略：

```text
project-templates/candidate-selection-policy.template.yaml
runtime/candidate_selection.py
```

基本流程：

```text
source agent frontmatter
  -> candidate
  -> candidate selection policy
  -> selected project candidates
  -> project team pack draft
  -> candidate review report
  -> promoted project team pack
```

这意味着 Awakening、Agent-team、think-tank 主仓或其他 Codex 项目都可以从同一个候选来源中挑不同专家，但不会互相污染队伍配置。

晋升入口：

```text
runtime/candidate_review.py
templates/candidate-review-report.md
```

晋升只改变项目级 team pack draft 中的 candidate 状态，不修改 `registries/global-experts.yaml`。

## Project Team Activation

项目 candidate 完成 review 后，还需要被激活成 leader 可见的 dispatch roster：

```text
runtime/project_team_activation.py
schemas/project-team-activation.schema.json
```

Activation 会合并两类队伍：

- `global_registry`：来自 `global-experts.yaml` 的基础专家。
- `project_candidate`：项目 team pack 中已 `promoted` 的候选 subagent。

未 review 的 candidate 不会进入 active roster。进入 roster 也仍然只是 `promoted_uninvoked`，不代表已经真实调用。

Codex leader orchestrator 可以选择性加载 promoted team pack：

```text
runtime/orchestrator.py --team-pack leader-runtime/examples/promoted-project-team-pack.sample.yaml
```

不传 `--team-pack` 时，leader 仍按全局 registry 和 think-tank Skill 结果运行；传入后，结果会额外包含 `project_team_activation`，并在 `leader_context.project_team` 中暴露当前项目队伍摘要。

## Project Candidate Dispatch Plan

激活后的 `project_candidate` 可以进入派遣计划，但仍不等于真实调用：

```text
runtime/project_candidate_dispatch.py
schemas/project-candidate-task-packet.schema.json
```

项目 candidate packet 会出现在 orchestrator 输出的 `project_candidate_task_packets` 中，状态固定为 `planned_uninvoked`。后续只有接入平台级 subagent invocation gate 后，才能从计划升级为真实调用证据。

## Runtime Entry

Codex leader runtime 的当前入口是：

```text
runtime/orchestrator.py
```

它作为上层调用方运行：

```text
leader-runtime orchestrator
  -> think-tank Codex Skill adapter
  -> expert registry / dispatch decision / task packets
  -> acceptance report
```

`think-tank/` 不应反向导入 `leader-runtime/`。

## 当前状态

```yaml
leader_runtime_boundary: established
think_tank_is_skill_core: true
codex_leader_blueprint: specified
codex_leader_runtime_helpers: implemented_partial
project_derived_leader_model: implemented_partial
project_team_pack_templates: implemented
global_expert_registry_data_source: implemented
candidate_selection_policy: implemented
candidate_review_gate: implemented
project_team_activation: implemented
project_aware_leader_orchestrator: implemented
project_candidate_dispatch_plan: implemented
```
