# Media Research Recipe

```yaml
intent: media_research
default_mode: research
core_question: "视频、播客、音频或长内容中有哪些可用信息和结论？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `这个视频讲了什么`
- `总结这个播客`
- `转录`
- `提取视频内容`
- `音频分析`
- `长内容摘要`

## Defaults

```yaml
profiles:
  - source-collector
  - report-architect
  - skeptic
capabilities:
  - media-processing
  - source-acquisition
# Provider selection is configured in .think-tank/provider-policy.yaml
fallback_inputs:
  - user_provided_transcript
  - user_provided_summary
  - local_media_metadata
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

1. 内容来源和处理方式。
2. 核心观点和证据。
3. 可引用片段或时间点。
4. 对用户任务的行动建议。
5. 未转录、不可访问或版权边界。

## Output

```text
结论
内容摘要
关键证据
可行动洞察
风险和边界
```
