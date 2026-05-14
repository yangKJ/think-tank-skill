# Intent Routing

本文定义 think-tank 如何从用户自然语言识别通用任务意图，并把意图映射到 mode、recipe、profiles 和 capabilities。

intent 是平台无关的任务语义。它不是具体工具、不是平台命令、不是旧 research agent 的私有触发词。

## 路由顺序

```text
user request
  -> intent detection
  -> mode selection
  -> recipe selection
  -> profile selection
  -> capability selection
  -> platform adapter execution
```

## 通用触发词

这些触发词适用于任何项目：

| 触发词 | intent | 默认 mode | 默认 recipe |
|--------|--------|-----------|-------------|
| `研究一下`、`帮我了解一下`、`查一下`、`调研一下` | `general_research` | `research` | `market-research` 或 `technical-research` |
| `深度研究`、`全面分析`、`系统分析`、`好好研究一下` | `deep_research` | `research` | 按主题选择 |
| `竞品分析`、`竞争分析`、`对比一下对手` | `competitive_intelligence` | `research` | `competitive-intelligence` |
| `市场调研`、`行业分析`、`用户需求` | `market_research` | `research` | `market-research` |
| `技术调研`、`方案调研`、`可行性分析` | `technical_research` | `research` | `technical-research` |
| `用户反馈`、`舆情分析`、`评论分析`、`社媒反馈` | `user_feedback_analysis` | `research` | `user-feedback-analysis` |
| `这个视频讲了什么`、`播客总结`、`转录后分析` | `media_research` | `research` | `media-research` |
| `开会讨论`、`讨论一下`、`帮我判断`、`是否应该` | `decision_council` | `council` | `decision-council` |
| `审查`、`review`、`验收`、`找问题` | `review_acceptance` | `review` | `review-acceptance` |
| `制定策略`、`路线图`、`优先级`、`行动方案` | `strategy_planning` | `strategy` | `strategy-planning` |
| `持续关注`、`监控方案`、`定期追踪` | `monitoring_plan` | `strategy` | `monitoring-plan` |
| `总结这些资料`、`汇总一下`、`提炼结论` | `synthesis` | `research` 或 `review` | `evidence-synthesis` |

## intent 与 mode 的关系

mode 决定输出形态，intent 决定任务配方。

```yaml
mode:
  answers: "这次用研究、审议、审查还是策略方式输出？"
intent:
  answers: "这次到底是在做哪类复杂任务？"
recipe:
  answers: "这类任务通常需要哪些角色、能力和质量门禁？"
```

同一个 intent 可以因用户要求进入不同 mode：

- `competitive_intelligence + research`：收集和分析竞品证据。
- `competitive_intelligence + council`：讨论是否跟进某个竞品策略。
- `competitive_intelligence + strategy`：制定竞争路线图。
- `competitive_intelligence + review`：审查已有竞品报告。

## recipe 选择规则

1. 用户显式说出任务类型时，优先选择对应 recipe。
2. 用户只说“研究一下”时，根据主题判断：
   - 产品、市场、用户、商业：`market-research`
   - 技术、架构、实现、库、模型：`technical-research`
   - 对手、替代品、竞品：`competitive-intelligence`
   - 评论、反馈、社媒：`user-feedback-analysis`
3. 用户请求包含“讨论/判断/是否应该”时，可选择 `decision-council`，并把原始主题作为 council 议题。
4. 用户请求包含“审查/验收/找问题”时，选择 `review-acceptance`。
5. 用户请求包含“长期/持续/监控/每周/定期”时，选择 `monitoring-plan`。

## peer skills 规则

recipe 可以列出 `optional_peer_skills`，但这只是候选实现。

```yaml
optional_peer_skills_are_dependencies: false
missing_peer_skill_behavior: degrade_to_core_protocol
installed_peer_skill_behavior: may_select_if_needed
execution_claim: only_verified_per_run
```

禁止：

- 把某个 recipe 写成必须依赖某个外部 skill。
- 把 `competitor_analysis`、`xiaohongshu`、`yt-dlp` 等工具写入 think-tank core 行为。
- 把 peer skill 文件存在说成已真实执行。

## 输出要求

当任务复杂或用户要求透明路由时，应输出：

```yaml
selected_intent:
selected_mode:
selected_recipe:
selected_profiles:
selected_capabilities:
candidate_peer_skills:
execution_method:
capability_status:
boundaries:
```

轻量任务可以不展示完整 YAML，但必须遵守同样的内部路由。
