# Claude Code Agent Mapping

本文定义旧 research agent subagents 如何映射到 think-tank profiles。

这些映射仅适用于 Claude Code 平台。think-tank core 只依赖 profiles，不依赖 `.claude/agents/*.md`。

## 映射表

| Claude Code subagent | think-tank profile | 说明 |
|----------------------|--------------------|------|
| `Research Sub Researcher` | `source-collector` | 外部资料、竞品情报、行业信息 |
| `Research Sub Trend Researcher` | `trend-analyst` | 趋势、市场、技术 scouting |
| `Research Sub Xiaohongshu Researcher` | `social-listener` | 小红书和社媒舆情 |
| `Research Sub Feedback Synthesizer` | `feedback-synthesizer` | 多渠道反馈综合 |
| `Research Sub Research Report Architect` | `report-architect` | 报告结构、洞察、建议 |
| `Research Sub Product Manager` | `product-strategist` | 产品判断、路线、优先级 |
| `Critic` | `skeptic` | 质疑、事实核查、风险审查 |
| `Feedback Synthesizer` | `report-architect` 或 `feedback-synthesizer` | 取决于任务输出类型 |

## profile 到 subagent 的映射流程

1. think-tank 根据协议选择 profiles。
2. Claude Code adapter 检查项目是否存在对应 `.claude/agents/*.md`。
3. 若存在，读取 agent 文件作为 prompt 来源。
4. 若不存在，使用 profile 文档生成平台 prompt。
5. 派发 subagent 后，必须回收结构化结果。
6. 未回收的 agent 结果必须在最终输出中标注边界。

## frontmatter 处理

旧 `.claude/agents/*.md` 中的 frontmatter 可以作为平台元数据：

- `name`
- `description`
- `tools`
- `color`
- `emoji`
- `vibe`

但 frontmatter 不能替代 profile 职责定义。adapter 必须读取正文并确认任务上下文。

## 领域绑定处理

旧 research agent 的 subagent 内容可能包含具体项目、固定竞品等领域知识。

迁移时应拆分：

- 通用职责：进入 `profiles/`
- 私有领域知识：留在具体项目自己的 domain pack 或本地资料中
- Claude Code 调用细节：留在本目录

## 能力状态

```yaml
agent_mapping_contract: planned
legacy_research_subagents: source_material
direct_subagent_execution: planned
result_recovery: planned
```

只有在真实执行并回收结果后，才能把具体映射标为 `verified`。
