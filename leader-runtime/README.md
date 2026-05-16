# leader-runtime

`leader-runtime/` 是本仓库中与 `think-tank/` 同级的主 agent 领导者运行层。

它不是一个高阶 Skill，也不是某个平台的零散脚本集合。

它负责定义：

- 主 agent 的领导者身份
- 全量专家池与项目裁剪专家池
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
├── runtime/
├── schemas/
└── templates/
```

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
```
