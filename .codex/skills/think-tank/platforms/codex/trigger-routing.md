# Codex Trigger Routing

本文定义旧 research agent 的触发词在 Codex 平台中的迁移规则。

## 核心原则

```yaml
router_owner: think-tank
old_research_agent_shell_required: false
external_skills_position: peer_skills
external_peer_skills_are_optional: true
think_tank_core_depends_on_peer_skills: false
trigger_input_style: natural_language
default_orchestrator: think-tank
```

旧 research agent 里的触发词可以继续使用，但不能再把用户请求直接路由到旧 research agent 身份。Codex 中的正确路径是：

```text
用户自然语言触发
  -> think-tank mode selection
  -> profiles selection
  -> capability slots
  -> optional peer skills when available and needed
  -> structured output
```

这里的 peer skills 只是候选实现，不是 think-tank 的组成部分。think-tank 的协议、mode、profiles、输出结构和质量门禁必须在没有任何外部 peer skill 时仍然可用。

## 旧触发词迁移表

| 用户说法 | 新 mode | profiles | capabilities | 候选同级 skills | 默认边界 |
|----------|---------|----------|--------------|-----------------|----------|
| `快速了解一下`、`简单看看`、`先了解一下`、`概况` | `research` | `source-collector`, `report-architect` | `source-acquisition` | `web-access`, `summarize` | 优先本地/用户材料；需要联网时先标注 |
| `研究一下`、`帮我了解一下`、`行业分析` | `research` | `source-collector`, `trend-analyst`, `report-architect`, `skeptic` | `source-acquisition`, `knowledge-persistence` | `research-workflow`, `omni-research`, `juejin-search`, `google-ai-mode-skill` | 不默认写 Obsidian |
| `深度研究`、`全面研究`、`系统分析`、`好好研究一下` | `research` | `source-collector`, `trend-analyst`, `social-listener`, `feedback-synthesizer`, `report-architect`, `skeptic` | `source-acquisition`, `social-listening`, `knowledge-persistence` | `omni-research`, `research-workflow`, `juejin-search`, `xiaohongshu`, `obsidian` | 需要真实联网/私有写入时单独标注 |
| `竞品分析`、`分析一下竞品`、`竞品动态` | `research` | `source-collector`, `trend-analyst`, `product-strategist`, `skeptic`, `report-architect` | `source-acquisition`, `social-listening`, `knowledge-persistence` | `competitor_analysis`, `web-access`, `juejin-search`, `xiaohongshu`, `social-media-analyzer`, `obsidian` | 竞品分析核心是新技术调研，不只是功能对比 |
| `小红书用户评价`、`舆情分析`、`用户反馈` | `research` | `social-listener`, `feedback-synthesizer`, `skeptic`, `report-architect` | `social-listening`, `source-acquisition` | `xiaohongshu`, `social-media-analyzer`, `summarize` | 不默认登录、不抓评论、不绕反爬 |
| `这个视频讲了什么`、`提取播客内容`、`转录` | `research` | `source-collector`, `report-architect` | `media-processing` | `yt-dlp`, `openai-whisper`, `xiaoyuzhou-transcribe`, `summarize` | 默认先用用户提供 transcript/summary |
| `解读 PDF`、`白皮书分析`、`报告解读` | `research` | `source-collector`, `trend-analyst`, `report-architect` | `source-acquisition` | `pdf-extraction`, `summarize` | 本地文件优先，外部链接需标注来源 |
| `构建知识图谱`、`沉淀知识` | `research` | `source-collector`, `report-architect`, `product-strategist` | `knowledge-persistence` | `knowledge-graph-builder`, `obsidian`, `notebooklm` | 不默认写私有库 |
| `持续监控`、`定期追踪`、`关注一下`、`监控` | `strategy` | `facilitator`, `source-collector`, `product-strategist`, `skeptic` | `source-acquisition`, `knowledge-persistence` | `taskflow`, `web-access`, `obsidian` | 在 Codex 中优先输出监控方案；自动化需用户明确授权 |
| `开会讨论`、`讨论一下`、`帮我判断` | `council` | `facilitator`, `product-strategist`, `skeptic`, `report-architect` | 按议题选择 | `think-tank` core first | Codex 默认 `single_agent_multi_profile_fallback`，除非显式使用 subagent runtime |
| `审查`、`验收`、`看看有没有问题` | `review` | `skeptic`, `report-architect`, `product-strategist` | 按材料选择 | `think-tank` core first | 先给问题和风险，不做泛泛总结 |

## 组合技能迁移

旧 `research-workflow` 的组合不迁入 think-tank core，而是变成 Codex trigger routing 的候选实现：

| 旧组合 | 新归属 |
|--------|--------|
| `web-access + summarize` | `source-acquisition` 的轻量实现候选 |
| `omni-research + juejin-search + competitor_analysis + obsidian` | `research mode` 的深度研究候选组合 |
| `xiaohongshu + social-media-analyzer + summarize` | `social-listening` 的舆情候选组合 |
| `pdf-extraction + knowledge-graph-builder + web-access` | `source-acquisition + knowledge-persistence` 的行业研究候选组合 |
| `yt-dlp + whisper + summarize` | `media-processing` 的视频/播客候选组合 |
| `taskflow + web-access + obsidian` | `strategy mode` 的持续监控候选组合 |

## Codex 测试说法

用户不需要记协议字段，可以直接说：

```text
研究一下 [主题]
```

Codex 应执行：

```yaml
selected_mode: research
selected_profiles:
  - source-collector
  - trend-analyst
  - report-architect
selected_capabilities:
  - source-acquisition
```

更明确的测试说法：

```text
用 think-tank research mode，按旧 research agent 的“深度研究”触发逻辑，研究 [主题]。
先做 capability/skill 路由说明，再执行；如果某个同级 skill 没有真实调用，就标注 not_verified。
输出结论、依据、分歧、风险、行动建议和边界。
```

竞品测试：

```text
竞品分析：[竞品/产品]。
用新的 think-tank 触发路由接管旧 research agent 的竞品分析逻辑。
重点不是普通功能对比，而是新技术调研、用户反馈、可借鉴策略和对我项目的优先级建议。
```

会议讨论测试：

```text
开会讨论：[议题]。
用 think-tank council mode，选择合适 profiles；在 Codex 中如果没有真实 subagent runtime，就明确标注 single_agent_multi_profile_fallback。
```

## 禁止过度声明

```yaml
installed_peer_skills: optional_snapshot_only
skill_trigger_routing: documented
external_skill_execution: must_be_verified_per_run
think_tank_core_depends_on_peer_skills: false
obsidian_write: requires_explicit_permission
login_or_social_scraping: requires_explicit_permission
true_parallel_subagents: requires_runtime_evidence
```

不能因为 `.codex/skills/` 里有某个 skill，就声称它已经完成真实执行。
