# project-templates

`project-templates/` 存放其他 Codex 项目派生主 agent 领导者时可直接复用的模板。

这些模板服务于：

- 项目 leader 身份定义
- 项目 team pack 裁剪
- 项目验收覆盖

## Files

- `candidate-selection-policy.template.yaml`
- `project-leader-pilot.template.yaml`
- `project-leader.template.yaml`
- `project-team-pack.template.yaml`

`candidate-selection-policy.template.yaml` 用于从本地 source agent frontmatter 中筛选项目自己的候选 subagent 队伍。筛选结果只是 team pack draft，必须经过 leader review 后才能 promotion。

promotion 后的 team pack 可以交给 `runtime/project_team_activation.py` 生成项目级 dispatch roster。未 promotion 的 candidate 不会被激活。

`project-leader-pilot.template.yaml` 用于其他 Codex 项目跑第一轮领导化试点。它把 request、selection policy、审核名单、candidate invocation readiness 和 host result 文件放进一份 spec，便于把“主 agent 升级成领导者”的落地动作标准化。
