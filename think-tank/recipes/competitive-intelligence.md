# Competitive Intelligence Recipe

```yaml
intent: competitive_intelligence
default_mode: research
core_question: "竞争对象做了什么、为什么有效、对当前项目有什么启发？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `竞品分析`
- `竞争分析`
- `对比一下对手`
- `替代品分析`
- `竞品动态`
- `这个产品为什么强`
- `我们和 X 差距在哪`

## Defaults

```yaml
profiles:
  - source-collector
  - trend-analyst
  - product-strategist
  - skeptic
  - report-architect
capabilities:
  - source-acquisition
  - social-listening
  - knowledge-persistence
optional_peer_skills:
  - web-access
  - summarize
  - social-media-analyzer
  - xiaohongshu
# Provider selection is configured in .think-tank/provider-policy.yaml
fallback_inputs:
  - user_provided_materials
  - local_files
  - model_reasoning_with_boundaries
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

1. 竞争对象和替代关系。
2. 核心能力、定位、用户群。
3. 新技术、流程或模式变化。
4. 用户反馈和市场信号。
5. 对当前项目的机会、风险和优先级建议。
6. 哪些信号足够进入 backlog，哪些仍只适合观察。

## Output

```text
结论
竞争对象概览
证据和来源
技术/产品/市场洞察
分歧与风险
行动建议
优先级判断
边界
```

## Quality Gates

- 不把营销话术当事实。
- 区分已验证信息、推断和建议。
- 每个行动建议都应能回答“为什么现在做”和“如何验证是否值得做”。
- 不因存在某个旧竞品分析脚本或工具，就绕过 think-tank 的 policy route、recipe、capability 和 quality gates。
- 如果没有外部来源，必须标注证据不足。

## Legacy Note

旧竞品分析编排职责已由 routing policy 取代。竞品方法论和报告结构应沉淀到本 recipe、templates 或 `.think-tank/domain-packs/`（domain-packs 已迁至本地配置目录），不再作为独立 provider。
