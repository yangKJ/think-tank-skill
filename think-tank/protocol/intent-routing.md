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
  -> routing/skill-router.md
  -> platform adapter execution
  -> routing/result-recovery.md
```

## 触发词配置

think-tank core 不内置固定触发词。

触发词属于 routing policy，由平台 adapter、项目本地配置或用户全局配置提供。协议层只定义 intent 语义，不规定用户必须说什么词。

```text
user request
  -> routing policy trigger matching
  -> intent
  -> mode
  -> recipe
  -> capabilities
```

policy 格式见：

```text
routing/policy-schema.md
```

平台可以提供 example policy 帮助用户快速开始，但 example policy 不是 core protocol。

## Intent Catalog

这些 intent 是平台无关语义，不是触发词：

| intent | 默认 mode | 默认 recipe |
|--------|-----------|-------------|
| `general_research` | `research` | `market-research` 或 `technical-research` |
| `deep_research` | `research` | 按主题选择 |
| `competitive_intelligence` | `research` | `competitive-intelligence` |
| `market_research` | `research` | `market-research` |
| `technical_research` | `research` | `technical-research` |
| `user_feedback_analysis` | `research` | `user-feedback-analysis` |
| `media_research` | `research` | `media-research` |
| `research_to_video` | `research` | `research-to-video` |
| `decision_council` | `council` | `decision-council` |
| `review_acceptance` | `review` | `review-acceptance` |
| `strategy_planning` | `strategy` | `strategy-planning` |
| `monitoring_plan` | `strategy` | `monitoring-plan` |
| `synthesis` | `research` 或 `review` | `evidence-synthesis` |
| `project_competitive_strategy` | `strategy` | `project-competitive-strategy` |

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

1. 用户显式指定 intent、mode 或 recipe 时，优先选择用户指定值。
2. routing policy 命中 route 时，使用 route 指定的 intent、mode、recipe、profiles 和 capabilities。
3. 用户只给宽泛研究请求时，根据主题判断：
   - 产品、市场、用户、商业：`market-research`
   - 技术、架构、实现、库、模型：`technical-research`
   - 对手、替代品、竞品：`competitive-intelligence`
   - 项目能力、竞品对比、差异化和市场进入：`project-competitive-strategy`
   - 评论、反馈、社媒：`user-feedback-analysis`
   - 选题研究、资料调研到视频成品：`research-to-video`
4. 没有 policy 或 policy 未命中时，平台 adapter 可使用保守默认策略。
5. 仍不能判断时，降级为 `general_research` 或询问用户。

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
- 把具体工具或平台私有 skill 写入 think-tank core 行为。
- 把 peer skill 文件存在说成已真实执行。

peer skill 的连接规则不写在 recipe 中，而写在：

```text
routing/skill-router.md
routing/dispatch-policy.md
routing/result-recovery.md
```

recipe 只声明“可能用哪些候选 skill”，routing 层才决定“本次是否选择、是否允许调用、如何降级和如何回收结果”。

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
