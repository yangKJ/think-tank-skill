# Strategy Backlog Brief

用于把 `think-tank` 的策略、调研或竞争分析结果整理成宿主 agent 可直接消费的 backlog 候选集。

## Required Fields

```yaml
mode: strategy | research
profiles:
  - "<profile>"
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

## Readiness Values

- `ready`
- `needs_input`
- `observe_only`
- `blocked`

## Template

```text
目标
- 本轮策略要解决什么问题

结论
- 最关键的方向判断

backlog 候选
- 标题：
  - readiness：
  - priority：
  - reason：
  - next_owner：
  - acceptance_criteria：
  - non_goals：
  - dependencies：
  - risk：

排序建议
- 为什么先做什么、后做什么

观察项
- 哪些值得持续关注，但当前不进入执行

验证计划
- 如何验证 backlog 候选是否成立

边界
- 哪些结论是已验证证据
- 哪些仍是策略性推断
```
