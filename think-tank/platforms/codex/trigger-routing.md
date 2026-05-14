# Codex Trigger Routing

本文定义 Codex 平台如何执行 think-tank 的通用 intent / recipe 路由。

平台无关的真相源是：

```text
protocol/intent-routing.md
recipes/
```

本文件只描述 Codex adapter 如何把这些通用路由落到当前项目的可选 peer skills。具体 peer skill 名称来自 Codex 本地 provider registry，不代表其他用户或其他项目默认拥有这些技能。

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

Codex 中的正确路径是：

```text
用户自然语言触发
  -> think-tank intent detection
  -> recipe selection
  -> mode selection
  -> profiles selection
  -> capability slots
  -> routing/skill-router.md
  -> platforms/codex/provider-registry.md
  -> optional providers when available and needed
  -> routing/result-recovery.md
  -> structured output
```

这里的 peer skills 只是候选实现，不是 think-tank 的组成部分。think-tank 的协议、mode、profiles、输出结构和质量门禁必须在没有任何外部 peer skill 时仍然可用。

Codex 适配层不得直接把触发词绑定到 peer skill。必须先通过：

```text
routing/skill-router.md
routing/dispatch-policy.md
routing/result-recovery.md
```

## Codex 触发路由表

下表中的候选同级 skills 是当前 Codex adapter 可识别的本地 provider 示例，不是 think-tank core 依赖。

| 用户说法 | intent | recipe | mode | 候选同级 skills | 默认边界 |
|----------|---------|----------|--------------|-----------------|----------|
| `快速了解一下`、`简单看看`、`先了解一下`、`概况` | `general_research` | `evidence-synthesis` | `research` | `web-access`, `summarize` | 优先本地/用户材料；需要联网时先标注 |
| `研究一下`、`帮我了解一下`、`行业分析` | `general_research` 或 `market_research` | `market-research` 或 `technical-research` | `research` | `research-workflow`, `omni-research`, `juejin-search`, `google-ai-mode-skill` | 不默认写 Obsidian |
| `深度研究`、`全面研究`、`系统分析`、`好好研究一下` | `deep_research` | 按主题选择 recipe | `research` | `omni-research`, `research-workflow`, `juejin-search`, `xiaohongshu`, `obsidian` | 需要真实联网/私有写入时单独标注 |
| `竞品分析`、`竞争分析`、`竞品动态` | `competitive_intelligence` | `competitive-intelligence` | `research` | `competitor_analysis`, `web-access`, `juejin-search`, `xiaohongshu`, `social-media-analyzer`, `obsidian` | 竞品分析核心是可迁移洞察，不只是功能对比 |
| `市场调研`、`用户需求`、`目标用户` | `market_research` | `market-research` | `research` | `web-access`, `summarize`, `36kr-hotlist`, `social-media-analyzer` | 市场数据需要来源或边界 |
| `技术调研`、`方案调研`、`可行性分析` | `technical_research` | `technical-research` | `research` | `web-access`, `summarize`, `juejin-search`, `pdf-extraction` | 区分事实、推断和实现建议 |
| `小红书用户评价`、`舆情分析`、`用户反馈` | `user_feedback_analysis` | `user-feedback-analysis` | `research` | `xiaohongshu`, `social-media-analyzer`, `summarize` | 不默认登录、不抓评论、不绕反爬 |
| `这个视频讲了什么`、`提取播客内容`、`转录` | `media_research` | `media-research` | `research` | `yt-dlp`, `openai-whisper`, `xiaoyuzhou-transcribe`, `summarize` | 默认先用用户提供 transcript/summary |
| `解读 PDF`、`白皮书分析`、`报告解读` | `technical_research` 或 `synthesis` | `technical-research` 或 `evidence-synthesis` | `research` | `pdf-extraction`, `summarize` | 本地文件优先，外部链接需标注来源 |
| `构建知识图谱`、`沉淀知识` | `synthesis` | `evidence-synthesis` | `research` | `knowledge-graph-builder`, `obsidian`, `notebooklm` | 不默认写私有库 |
| `持续监控`、`定期追踪`、`关注一下`、`监控` | `monitoring_plan` | `monitoring-plan` | `strategy` | `taskflow`, `web-access`, `obsidian` | 在 Codex 中优先输出监控方案；自动化需用户明确授权 |
| `开会讨论`、`讨论一下`、`帮我判断` | `decision_council` | `decision-council` | `council` | `think-tank` core first | Codex 默认 `single_agent_multi_profile_fallback`，除非显式使用 subagent runtime |
| `审查`、`验收`、`看看有没有问题` | `review_acceptance` | `review-acceptance` | `review` | `think-tank` core first | 先给问题和风险，不做泛泛总结 |

## 组合技能迁移

旧 `research-workflow` 的组合不迁入 think-tank core，而是变成 recipe 的候选实现：

| 旧组合 | 新归属 |
|--------|--------|
| `web-access + summarize` | `source-acquisition` 的轻量实现候选 |
| `omni-research + juejin-search + competitor_analysis + obsidian` | `competitive-intelligence` 或深度研究 recipe 的候选组合 |
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
selected_intent: general_research
selected_recipe: market-research 或 technical-research
selected_profiles:
  - source-collector
  - trend-analyst
  - report-architect
selected_capabilities:
  - source-acquisition
```

更明确的测试说法：

```text
用 think-tank research mode，按通用 intent/recipe 路由，研究 [主题]。
先做 capability/skill 路由说明，再执行；如果某个同级 skill 没有真实调用，就标注 not_verified。
输出结论、依据、分歧、风险、行动建议和边界。
```

竞品测试：

```text
竞品分析：[竞品/产品]。
用 think-tank 的 competitive-intelligence recipe。
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
