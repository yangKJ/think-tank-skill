# Research Migration Audit

本文核对旧 research agent 是否已经迁移到统一 think-tank 主仓。

来源：

```text
legacy research workspace
```

## 结论

```yaml
migration_status: core_capabilities_migrated
legacy_think_tank_status: fully_migrated_by_abstraction
not_status: full_archive_copied
judgement: sufficient_for_think_tank_v0_2
```

旧 research agent 的通用能力已经迁移到 think-tank 的抽象层：

- `research mode`
- `profiles`
- `capabilities`
- `platforms/claude-code`
- `domain-packs` 扩展点
- `runtime/safety.py`
- `templates/`

但旧 research 目录里的历史知识库、运行记录、日志、agent memory 和项目报告没有全部迁入，也不应全部进入 core。

旧 `.claude/skills/think-tank` 的完整迁移处置见：

```text
docs/legacy-think-tank-full-migration.md
```

## 已迁移到位

### 1. Subagents 到 Profiles

| 旧 research subagent | 新位置 |
|----------------------|--------|
| `Research Sub Researcher` | `profiles/source-collector.md` |
| `Research Sub Trend Researcher` | `profiles/trend-analyst.md` |
| `Research Sub Xiaohongshu Researcher` | `profiles/social-listener.md` |
| `Research Sub Feedback Synthesizer` | `profiles/feedback-synthesizer.md` |
| `Research Sub Research Report Architect` | `profiles/report-architect.md` |
| `Research Sub Product Manager` | `profiles/product-strategist.md` |
| `Critic` | `profiles/skeptic.md` |

平台映射记录在：

```text
platforms/claude-code/agent-mapping.md
```

### 2. Skills 到 Capabilities

| 旧 skill 类别 | 新 capability |
|---------------|----------------|
| `web-access`、`google-ai-mode-skill`、`juejin-search`、`36kr-hotlist`、`mcp-cli` | `source-acquisition` |
| `playwright-cli`、`web-access` | `browser-automation` |
| `xiaohongshu`、`social-media-analyzer` | `social-listening` |
| `yt-dlp`、`openai-whisper`、`xiaoyuzhou-transcribe`、`summarize` | `media-processing` |
| `obsidian`、`notebooklm`、`knowledge-graph-builder`、`taskflow` | `knowledge-persistence` |

平台映射记录在：

```text
platforms/claude-code/skill-mapping.md
```

### 3. Research 工作方式到 Mode

已吸收的旧能力：

- 快速概览
- 深度研究
- 多渠道采集
- 交叉验证
- 报告生成
- 知识沉淀
- 持续监控
- 自主研究循环

记录位置：

```text
docs/research-agent-capability-map.md
modes/research.md
```

### 4. 私有领域经验不进入主仓

旧 research 中绑定具体产品、固定竞品、平台私有数据和领域报告的内容不进入当前主仓。需要这些知识的项目应在自己的仓库中维护 domain pack 或本地资料目录。

## 没有原样迁移的内容

以下内容没有迁入主仓 core，这是有意保留边界：

### 1. 历史知识库

旧路径：

```text
knowledge/
```

当前数量：约 36 个 Markdown/资料文件。

判断：

- 不属于 think-tank core。
- 可作为具体项目自己的 domain pack 或外部知识库素材。
- 不应默认打包进通用 Skill。

### 2. 运行记录和旧输出

旧路径：

```text
.think-tank/conclusions/
.think-tank/discuss-*/
.think-tank/runs/current/
shared/results/
```

判断：

- 已抽象其运行形态和结果结构。
- 不应把旧运行结果当协议真相源。
- 可筛选少量匿名化样例进入 `examples/`，但不是 v0.1 必需。

### 3. Agent memory

旧路径：

```text
.claude/agent-memory/
memory/
```

判断：

- 已吸收其中关于 mock、tracking、Claude Code Team 限制的结论。
- 不应把历史 memory 原文迁入主协议。
- 如后续需要，可做 `docs/legacy-lessons.md`，只保留经验总结。

### 4. 平台私有配置

旧路径：

```text
.claude/settings.json
.claude/settings.local.json
.claude/scheduled_tasks.json
.playwright-cli/
logs/
```

判断：

- 属于旧 research 运行环境，不属于跨平台 Skill。
- 不迁入。

## 仍可选补充的迁移项

这些不是当前缺口，但可作为后续增强：

```yaml
optional_backlog:
  - 从旧 knowledge 中筛选 2 到 3 个匿名化 research output 样例
  - 将旧 daily briefing 抽象为 continuous_monitoring example
  - 将旧 .think-tank/discuss 输出抽象为 council/research hybrid example
  - 将旧 agent-memory 的经验整理成 legacy lessons
```

## 最终判断

```yaml
research_core_migration: complete_for_v0_2
legacy_think_tank_migration: complete
research_archive_migration: intentionally_not_copied
core_protocol_dependency_on_old_research: none
old_research_parent_status: removed
next_action: optional_example_curation_only
```

当前 think-tank 已经完成对旧 research agent 的核心能力迁移。剩余旧资料应作为可选样例或领域知识库筛选，不应继续阻塞主仓建设。
