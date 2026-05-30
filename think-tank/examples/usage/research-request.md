# Research Request Example

## 输入

```yaml
task: "研究某个开源项目是否适合作为主仓依赖"
mode: research
context:
  - "需要评估维护活跃度、许可证、API 稳定性和替代方案"
constraints:
  - "只能使用公开信息"
success_criteria:
  - "给出是否采用的建议"
  - "列出主要风险和后续验证步骤"
evidence_policy:
  network: required
  local_sources: allowed
  citations: required
output_preference: report
```

## 输出结构

```text
结论
依据
角色观点
分歧与风险
行动建议
边界
```

