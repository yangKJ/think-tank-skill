# Research Action Brief

用于把调研、竞品、趋势或用户反馈结论收口成宿主 agent 可直接消费的动作简报。

## Required Fields

```yaml
mode: research | strategy
profiles:
  - "<profile>"
capabilities:
  - "<capability>"
runtime_provenance:
  think_tank_runtime_used: true | false
  provider_policy_checked: true | false
  dispatch_decision_emitted: true | false
  provider_invoked: true | false
  result_recovered: true | false
  true_multi_agent_runtime: true | false
  execution_method: full_runtime | adapter_runtime | direct_tool_call | single_agent_multi_profile | manual_synthesis | protocol_only
  data_collection: provider_managed | direct_assistant_tool | user_provided | local_files | none
  evidence_state: planned | mock | installed | discovered | selected | dispatched | invoked | recovered | verified_partial | verified | blocked | failed | tracking
  result_recovery: automatic | manual | none
  boundaries: []
```

## Template

```text
任务
- 本次研究要回答什么问题

结论
- 最重要的 1-3 条结论

关键证据
- 证据 1：来源 + 为什么重要
- 证据 2：来源 + 为什么重要

影响判断
- 对当前项目/策略/产品的直接影响

建议动作
- P0：
  - 动作
  - 原因
  - 验证方式
- P1：
  - 动作
  - 原因
  - 验证方式

暂不行动
- 哪些信号值得记录，但现在不应执行

非目标
- 这次建议明确不包含什么

分歧与风险
- 主要反对意见或证据不足点

边界
- 哪些部分来自验证证据
- 哪些部分仍是推断
```
