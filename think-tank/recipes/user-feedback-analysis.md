# User Feedback Analysis Recipe

```yaml
intent: user_feedback_analysis
default_mode: research
core_question: "用户真实反馈说明了什么需求、痛点和风险？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `用户反馈`
- `评论分析`
- `舆情分析`
- `小红书用户评价`
- `社媒反馈`
- `用户怎么说`
- `口碑分析`

## Defaults

```yaml
profiles:
  - social-listener
  - feedback-synthesizer
  - skeptic
  - report-architect
capabilities:
  - social-listening
  - source-acquisition
optional_peer_skills:
  - xiaohongshu
  - social-media-analyzer
  - summarize
  - web-access
fallback_inputs:
  - pasted_comments
  - exported_reviews
  - local_feedback_files
```

## Runtime Provenance

```yaml
runtime_provenance:
  think_tank_runtime_used: "{true|false}"
  provider_policy_checked: "{true|false}"
  dispatch_decision_emitted: "{true|false}"
  provider_invoked: "{true|false}"
  result_recovered: "{true|false}"
  true_multi_agent_runtime: "{true|false}"
  execution_method: "{full_runtime|adapter_runtime|direct_tool_call|single_agent_multi_profile|manual_synthesis|protocol_only}"
  data_collection: "{provider_managed|direct_assistant_tool|user_provided|local_files|none}"
  evidence_state: "{selected|invoked|recovered|verified_partial|verified|blocked|failed|tracking}"
  result_recovery: "{automatic|manual|none}"
  boundaries: []
```

## Required Analysis

1. 样本来源和代表性。
2. 高频需求、痛点和情绪。
3. 用户分群差异。
4. 可转化为产品行动的机会。
5. 样本偏差和不可验证部分。

## Safety

- 不默认登录平台。
- 不绕过反爬或访问私密内容。
- 不把小样本当总体结论。

## Output

```text
结论
样本说明
反馈主题
用户洞察
风险与偏差
行动建议
边界
```
