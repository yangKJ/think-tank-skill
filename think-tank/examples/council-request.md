# Council Request Example

## 输入

```yaml
task: "讨论是否应该把旧 agent-council 作为独立项目继续维护"
mode: council
context:
  - "think-tank 是新的统一主 Skill"
  - "agent-council 是历史妥协实现"
constraints:
  - "不能让旧实现继续主导新协议"
success_criteria:
  - "形成明确决策"
  - "给出迁移路径"
evidence_policy:
  network: disallowed
  local_sources: required
  citations: optional
output_preference: decision
```

## 期望输出

- 共识结论
- 少数意见
- 关键风险
- 迁移行动
- 不应继续投入的方向

