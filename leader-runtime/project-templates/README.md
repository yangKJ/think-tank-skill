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

promotion 后的 team pack 可以交给 `runtime/project_team_activation.py` 生成项目级 dispatch roster。未 promotion 的 candidate 不会被激活。
