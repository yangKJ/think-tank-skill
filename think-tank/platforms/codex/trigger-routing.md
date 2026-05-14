# Codex Trigger Routing

本文定义 Codex 平台如何执行 think-tank 的通用 intent / recipe 路由。

平台无关的真相源是：

```text
protocol/intent-routing.md
recipes/
```

本文件只描述 Codex adapter 如何把 routing policy 命中的 intent/recipe/capability 落到当前项目的可选 peer skills。具体触发词和 peer skill 名称来自 Codex 本地 provider policy 与 provider registry，不代表其他用户或其他项目默认拥有这些配置。

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
  -> platforms/codex/provider-policy.example.yaml or .codex/think-tank.provider-policy.yaml
  -> selected intent / recipe / mode / profiles / capability slots
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

## Codex Policy

Codex 默认示例配置位于：

```text
platforms/codex/provider-policy.example.yaml
```

项目本地可复制为：

```text
.codex/think-tank.provider-policy.yaml
```

本地 policy 不上传 GitHub。用户可以在该文件中定义触发词、intent、recipe、capability 和 provider 偏好。

例如用户希望“上网研究”只允许小红书 provider，可以在本地 policy 中配置：

```yaml
routes:
  - id: xiaohongshu-only-research
    priority: 100
    enabled: true
    triggers:
      match: regex
      patterns:
        - "(上网研究|研究一下)"
    intent: user_feedback_analysis
    mode: research
    recipe: user-feedback-analysis
    capabilities:
      - social-listening
      - source-acquisition
    providers:
      prefer:
        - xiaohongshu
      allow:
        - xiaohongshu
      deny:
        - web-access
        - google-ai-mode-skill
    fallback: ask_user
```

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
