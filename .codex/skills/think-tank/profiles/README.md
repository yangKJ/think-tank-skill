# profiles

`profiles/` 定义 think-tank 的跨平台角色模板。

profile 不是 Claude Code subagent 文件，也不是固定 prompt。它描述一个角色在 think-tank 协议中的使命、输入、输出、能力、质量标准和禁止行为。

平台 adapter 可以把 profile 映射为：

- Claude Code subagent
- Codex 单 agent 分段执行
- 外部 agent runtime
- 人工执行步骤
- 脚本或工具链

## 第一批 profiles

- `facilitator.md`：主持人和流程协调者
- `source-collector.md`：资料和证据收集者
- `trend-analyst.md`：趋势和机会分析者
- `social-listener.md`：社媒和用户反馈监听者
- `feedback-synthesizer.md`：多渠道反馈综合者
- `report-architect.md`：报告和结论结构化者
- `skeptic.md`：质疑、事实核查和风险审查者
- `product-strategist.md`：产品、路线和优先级判断者

## 与旧 subagents 的关系

旧 research agent 中的 subagents 是这些 profile 的来源材料，但不直接进入 core。

Claude Code 的 `.claude/agents/*.md`、`subagent_type`、frontmatter 和工具字段都属于平台适配，不属于 profile 本身。

