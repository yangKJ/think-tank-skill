# project-templates

`project-templates/` 存放其他 Codex 项目派生主 agent 领导者时可直接复用的模板。

这些模板服务于：

- 项目 leader 身份定义
- 项目 team pack 裁剪
- 项目验收覆盖

## Files

- `candidate-selection-policy.template.yaml`
- `project-leader.template.yaml`
- `project-team-pack.template.yaml`

`candidate-selection-policy.template.yaml` 用于从本地 source agent frontmatter 中筛选项目自己的候选 subagent 队伍。筛选结果只是 team pack draft，必须经过 leader review 后才能 promotion。
