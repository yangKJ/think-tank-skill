# Review Acceptance Recipe

```yaml
intent: review_acceptance
default_mode: review
core_question: "这个产物是否正确、完整、可验收，还有哪些问题？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `审查`
- `review`
- `验收`
- `找问题`
- `看看有没有漏洞`
- `是否完成`
- `质量如何`

## Defaults

```yaml
profiles:
  - skeptic
  - report-architect
  - product-strategist
capabilities:
  - source-acquisition
optional_peer_skills:
  - summarize
  - pdf-extraction
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

1. 验收对象和标准。
2. 发现的问题，按严重程度排序。
3. 证据、文件或材料定位。
4. 修复建议。
5. 残余风险。

## Output

```text
问题清单
验收结论
依据
修复建议
残余风险
边界
```
