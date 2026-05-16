# Research Agent Full Inventory

本文逐项记录旧 research agent 的资产分类和迁移去向。

来源：

```text
legacy research workspace
```

## 目录级处置

| 旧目录或文件 | 当前处置 | 新位置 |
|--------------|----------|--------|
| `CLAUDE.md` | Claude Code 平台说明，不进入 core | `platforms/claude-code/` 文档吸收 |
| `AGENTS.md` | 旧项目本地协作规则，不进入主仓发布内容 | 不迁移 |
| `.claude/agents/` | 全部映射为 think-tank profiles | `profiles/`、`platforms/claude-code/agent-mapping.md` |
| `.claude/skills/` | 全部映射为 capability 或外部 skill 互操作 | `capabilities/`、`platforms/claude-code/skill-mapping.md`、`docs/external-skill-interoperability.md` |
| `.claude/skills/think-tank/` | 已完成旧 think-tank 全量迁移 | `docs/legacy-think-tank-full-migration.md` |
| `knowledge/` | 私有领域研究知识，不进入当前主仓 | 由具体项目自行维护 |
| `logs/daily/` | 监控简报样例来源 | `templates/monitoring-brief.md` |
| `memory/` | 历史经验来源，抽象为迁移结论 | `docs/research-migration-audit.md` |
| `.claude/agent-memory/` | 旧 think-tank issue 和 UX 经验 | `docs/legacy-think-tank-full-migration.md`、`docs/legacy-runtime-safety.md` |
| `.think-tank/` | 旧运行产物，不作为协议真相源 | `examples/` 中已有精选验证样例 |
| `shared/results/` | 旧 agent 输出形态来源 | `templates/evidence-table.md`、`templates/expert-meeting.md` |
| `.playwright-cli/`、`.playwright/` | 平台工具缓存和日志 | 不迁移 |
| `.claude/settings*.json` | 私有平台配置和密钥风险 | 不迁移 |
| `.claude/scheduled_tasks.json` | 旧定时任务配置 | 抽象为 `continuous_monitoring` |

## Agents

| 旧 agent | 新 profile | 状态 |
|----------|------------|------|
| `Research Sub Researcher` | `source-collector` | migrated |
| `Research Sub Trend Researcher` | `trend-analyst` | migrated |
| `Research Sub Xiaohongshu Researcher` | `social-listener` | migrated |
| `Research Sub Feedback Synthesizer` | `feedback-synthesizer` | migrated |
| `Research Sub Research Report Architect` | `report-architect` | migrated |
| `Research Sub Product Manager` | `product-strategist` | migrated |
| `Critic` | `skeptic` | migrated |

## Skills

| 旧 skill | 分类 | 新去向 | 状态 |
|----------|------|--------|------|
| `36kr-hotlist` | news/trend feed | `source-acquisition` | mapped |
| `apple-reminders` | personal reminder/task app | out-of-core, optional external skill | classified |
| `google-ai-mode-skill` | web research | `source-acquisition` | mapped |
| `juejin-search` | community source | `source-acquisition` | mapped |
| `knowledge-graph-builder` | knowledge structure | `knowledge-persistence` | mapped |
| `mcp-cli` | dynamic tool discovery | `source-acquisition` / platform adapter | mapped |
| `notebooklm` | knowledge notebook | `knowledge-persistence` | mapped |
| `obsidian` | knowledge base write | `knowledge-persistence` | mapped |
| `omni-research` | autonomous research loop | `research mode: autonomous_research` | migrated |
| `openai-whisper` | audio transcription | `media-processing` | mapped |
| `pdf-extraction` | document extraction | `source-acquisition` | mapped |
| `playwright-cli` | browser automation | `browser-automation` | mapped |
| `research-workflow` | legacy research route wrapper | `modes/research.md` / `platforms/codex/trigger-routing.md` / provider policy | deleted_and_replaced |
| `social-media-analyzer` | social metrics | `social-listening` | mapped |
| `stable-diffusion-image-generation` | image generation tool | out-of-core, optional external skill | classified |
| `summarize` | URL/file/media summary | `source-acquisition` / `media-processing` | mapped |
| `taskflow` | long-running task state | `knowledge-persistence` / runtime state | mapped |
| `think-tank` | old council/research runtime | `docs/legacy-think-tank-full-migration.md` | migrated |
| `using-tmux-for-interactive-commands` | interactive CLI helper | platform adapter only | classified |
| `vision-analysis` | image understanding | `media-processing` / evidence extraction | mapped |
| `web-access` | web and CDP browser | `source-acquisition` / `browser-automation` | mapped |
| `xiaohongshu` | RedNote social listening | `social-listening` | mapped |
| `xiaoyuzhou-transcribe` | podcast transcription | `media-processing` | mapped |
| `yt-dlp` | video/audio download | `media-processing` | mapped |

## Knowledge

旧 `knowledge/` 下的 Markdown 资料属于私有领域知识或历史报告，不进入当前通用主仓。需要这些知识的项目应在自己的仓库中添加 domain pack 或本地资料目录。

## Logs 和 Memory

旧 logs/memory 的迁移策略：

- daily briefing 的结构进入 `templates/monitoring-brief.md`。
- discussion result 的结构进入 `templates/expert-meeting.md` 和 `templates/evidence-table.md`。
- issue 和 UX 改进记忆进入迁移审计，不复制原文。
- 私有路径、个人状态、历史运行缓存不进入发布内容。

## 状态

```yaml
agents_disposed: 7
skills_disposed: 24
private_domain_knowledge_in_core: false
legacy_logs_disposed: true
legacy_memory_disposed: true
private_platform_config_excluded: true
research_agent_migration_status: complete
```
