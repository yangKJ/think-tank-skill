# Evidence Synthesis Recipe

```yaml
intent: synthesis
default_mode: research
core_question: "如何把已有资料综合成清晰结论和行动建议？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `总结这些资料`
- `汇总一下`
- `提炼结论`
- `整理成报告`
- `归纳重点`

## Defaults

```yaml
profiles:
  - source-collector
  - report-architect
  - skeptic
capabilities:
  - source-acquisition
  - knowledge-persistence
optional_peer_skills:
  - summarize
  - pdf-extraction
  - obsidian
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

1. 资料范围。
2. 事实、推断和建议分离。
3. 证据强弱。
4. 冲突和不确定性。
5. 可执行结论。

## Output

```text
结论
证据整理
冲突和不确定性
建议
边界
```
