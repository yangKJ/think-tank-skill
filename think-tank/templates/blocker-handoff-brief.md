# Blocker Handoff Brief

用于在 `think-tank` 讨论、审查或策略收口后，明确阻塞类型、下一 owner 和交接完整性。

## Required Fields

```yaml
mode: review | strategy | council
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

## Blocker Types

- `information`
- `dependency`
- `environment`
- `execution`

## Template

```text
当前目标
- 任务要达成什么

当前状态
- 已完成什么
- 还未完成什么

阻塞分类
- 类型：information | dependency | environment | execution
- 原因：

当前 owner
- 谁当前持有问题

下一 owner
- 谁最适合接手推进

需要交接的内容
- 交付物
- 当前状态
- 对方要做什么
- 还缺什么

升级判断
- 是否应立即升级：yes | no
- 理由：

建议动作
- 现在最合理的下一步

边界
- 当前判断不覆盖什么
```
