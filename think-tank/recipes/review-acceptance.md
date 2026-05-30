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
# Provider selection is configured in .think-tank/provider-policy.yaml
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
4. 当前是否具备进入下一阶段或交付的条件。
5. 如果未通过，卡点属于信息、依赖、环境还是执行。
6. 修复建议、下一 owner 和残余风险。

## Output

```text
问题清单
验收结论
依据
阶段 readiness
修复建议
下一步与 owner
残余风险
边界
```

## Quality Gates

- 不把“部分可用”包装成“已通过验收”。
- 如果未通过，应说明阻塞类型，而不只说“还有问题”。
- 如果建议继续推进，应明确当前 readiness 依据。
