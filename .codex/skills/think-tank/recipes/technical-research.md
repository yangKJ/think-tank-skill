# Technical Research Recipe

```yaml
intent: technical_research
default_mode: research
core_question: "某项技术、方案或架构是否可行，应该如何落地？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `技术调研`
- `方案调研`
- `可行性分析`
- `架构方案`
- `实现路径`
- `选型`
- `性能/成本/风险`

## Defaults

```yaml
profiles:
  - source-collector
  - trend-analyst
  - skeptic
  - report-architect
capabilities:
  - source-acquisition
  - knowledge-persistence
optional_peer_skills:
  - web-access
  - summarize
  - google-ai-mode-skill
  - juejin-search
  - pdf-extraction
  - knowledge-graph-builder
```

## Required Analysis

1. 技术原理和适用边界。
2. 实现路径和依赖条件。
3. 性能、成本、维护和安全风险。
4. 替代方案比较。
5. 推荐方案和验证步骤。

## Output

```text
结论
方案概述
依据
替代方案
风险
落地步骤
边界
```
