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
  - juejin-search
  - xiaohongshu
  - social-media-analyzer
  - obsidian
fallback_inputs:
  - user_provided_materials
  - local_files
  - model_reasoning_with_boundaries
```

## Required Analysis

1. 竞争对象和替代关系。
2. 核心能力、定位、用户群。
3. 新技术、流程或模式变化。
4. 用户反馈和市场信号。
5. 对当前项目的机会、风险和优先级建议。

## Output

```text
结论
竞争对象概览
证据和来源
技术/产品/市场洞察
分歧与风险
行动建议
边界
```

## Quality Gates

- 不把营销话术当事实。
- 区分已验证信息、推断和建议。
- 不因存在某个旧竞品分析脚本或工具，就绕过 think-tank 的 policy route、recipe、capability 和 quality gates。
- 如果没有外部来源，必须标注证据不足。

## Legacy Note

旧竞品分析编排职责已由 routing policy 取代。竞品方法论和报告结构应沉淀到本 recipe、templates 或 domain-packs，不再作为独立 provider。
