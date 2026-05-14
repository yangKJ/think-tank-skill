# Recipes

`recipes/` 定义跨项目、跨平台可复用的任务配方。

recipe 不是外部 skill，也不是平台 adapter。它只回答：

- 这类任务通常是什么 intent？
- 默认应该用什么 mode？
- 需要哪些 profiles？
- 需要哪些 capabilities？
- 可以选择哪些可选 peer skills？
- 输出和质量门禁是什么？

## 边界

```yaml
recipes_are_protocol_assets: true
recipes_are_tool_implementations: false
optional_peer_skills_are_dependencies: false
missing_peer_skill_behavior: degrade_to_core_protocol
```

think-tank 在没有任何外部 peer skill 的情况下，也必须能执行 recipe 的核心推理、角色分析、边界声明和行动建议输出。

## 文件

- `competitive-intelligence.md`：竞争、竞品、替代方案分析。
- `market-research.md`：市场、行业、用户需求研究。
- `technical-research.md`：技术方案、架构、可行性研究。
- `user-feedback-analysis.md`：用户反馈、评论、舆情分析。
- `media-research.md`：视频、播客、音频、长内容研究。
- `decision-council.md`：多角色会议、决策审议。
- `review-acceptance.md`：审查、验收、质量判断。
- `strategy-planning.md`：路线图、优先级、行动方案。
- `monitoring-plan.md`：持续关注、监控指标、定期追踪方案。
- `evidence-synthesis.md`：资料汇总、证据综合、结论提炼。
