# schemas

`leader-runtime/schemas/` 存放主 agent 领导者系统的机器可读契约。

这里不存放 `think-tank` 的 Skill 输入输出 schema，而只存放：

- 专家注册表
- dispatch decision
- expert task packet
- acceptance report
- project leader
- project team pack
- source agent frontmatter candidate
- candidate selection policy
- candidate selection result
- candidate review report
- project team activation
- project candidate task packet

这些 schema 服务于领导者运行层，不属于 `think-tank` 高阶 Skill core。

当前全局专家池数据源是 `../registries/global-experts.yaml`，其输出结构应符合 `expert-role-registry.schema.json` 的核心字段要求。项目派生 registry 则由 `runtime/project_derivation.py` 基于全局 registry 和 team pack 生成。

`source-agent-frontmatter.schema.json` 只描述从 Claude Code agent frontmatter 解析出来的候选输入。它不是最终专家注册表；candidate 必须经过审核后才能进入 `registries/global-experts.yaml` 或项目 team pack。

`candidate-selection-policy.schema.json` 和 `candidate-selection-result.schema.json` 描述项目如何从候选源中筛出自己的 subagent 队伍。它们服务项目级 team pack 草案，不改变全局专家池。

`candidate-review-report.schema.json` 描述 leader 对候选队伍的晋升门禁。只有 review report 通过后，candidate 才能在项目 team pack 中从 `candidate` 变为 `promoted`。

`project-team-activation.schema.json` 描述项目 team pack 被加载成 dispatch roster 后的结构。它只表示 leader 可以看见哪些专家，不表示这些专家已被调用。

`project-candidate-task-packet.schema.json` 描述 promoted project candidate 的任务计划。它的状态应保持 `planned_uninvoked`，直到平台 runtime 提供真实 invocation evidence。
