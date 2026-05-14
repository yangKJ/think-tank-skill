# Input and Output Contract

## 输入字段

```yaml
task: ""
mode: research | council | review | strategy | auto
context: []
constraints: []
success_criteria: []
evidence_policy:
  network: allowed | disallowed | required
  local_sources: allowed | required
  citations: optional | required
output_preference: report | plan | review | decision | checklist
```

## 输出字段

```yaml
mode: ""
roles: []
conclusion: ""
evidence: []
role_views: []
disagreements: []
risks: []
recommendations: []
boundaries: []
next_steps: []
quality_check:
  protocol_complete: true
  evidence_boundary_clear: true
  actionable: true
```

## 兼容要求

平台适配可以把这些字段映射成 Markdown、JSON、YAML、任务文件或平台原生命令，但语义不能改变。

