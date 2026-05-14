# Decision Council Recipe

```yaml
intent: decision_council
default_mode: council
core_question: "多个角色如何审议一个复杂判断并形成可执行结论？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `开会讨论`
- `讨论一下`
- `帮我判断`
- `是否应该`
- `正反意见`
- `观点碰撞`
- `专家组`

## Defaults

```yaml
profiles:
  - facilitator
  - product-strategist
  - skeptic
  - report-architect
capabilities: []
optional_peer_skills: []
```

## Required Analysis

1. 明确议题和决策标准。
2. 分角色独立观点。
3. 共识、分歧和 blocking objection。
4. 裁决或推荐路径。
5. 后续验证动作。

## Output

```text
结论
角色观点
共识
分歧与风险
裁决
行动建议
边界
```
