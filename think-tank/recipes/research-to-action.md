# Research To Action Recipe

```yaml
intent: research_to_action
default_mode: strategy
core_question: "这些研究结论到底意味着什么，下一步应该做什么？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `把调研转成行动`
- `下一步怎么做`
- `整理成可执行建议`
- `转成 backlog`
- `给我明确动作`
- `把结论落地`

## Defaults

```yaml
profiles:
  - source-collector
  - report-architect
  - product-strategist
  - skeptic
capabilities:
  - source-acquisition
  - knowledge-persistence
optional_peer_skills:
  - web-access
  - summarize
  - obsidian
  - apple-reminders
# Provider selection is configured in .think-tank/provider-policy.yaml
fallback_inputs:
  - local_files
  - user_provided_materials
  - prior_think_tank_outputs
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

1. 哪些结论是硬事实，哪些只是强推断。
2. 每条关键结论对当前项目的影响是什么。
3. 哪些动作值得立刻做，哪些应延后观察。
4. 每个动作的优先级、非目标、验证方式和主要风险。
5. 是否需要把结论进入 `strategy_to_backlog` 结构。

## Output

```text
结论
关键证据
影响判断
行动建议
backlog 候选
风险与边界
```

## Quality Gates

- 不把研究结论直接包装成已经验证的产品决策。
- 不给没有证据支撑的动作高优先级。
- 动作建议必须说明目标、非目标和验证方式。
- 如果证据只够支持继续观察，必须明确写出“继续观察”，而不是强行给执行项。
