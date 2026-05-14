# Result Recovery

本文定义 peer skill 调用结果如何回收到 think-tank 的统一输出结构。

## Recovery Targets

```yaml
recovery_targets:
  sources: "来源、URL、文件、材料"
  evidence: "支持结论的证据"
  role_result: "某个 profile 的结构化判断"
  artifacts: "生成的报告、摘要、图谱、转录"
  boundaries: "未验证、失败、降级和权限边界"
```

## Minimum Recovery Record

```yaml
recovery:
  peer_skill: ""
  capability: ""
  invocation_status: success | failed | skipped
  result_recovered: true | false
  recovered_as: []
  source_count: 0
  evidence_count: 0
  boundaries: []
```

## Mapping Rules

### source-acquisition

```yaml
maps_to:
  - sources[]
  - evidence[]
  - boundaries[]
```

### social-listening

```yaml
maps_to:
  - sources[]
  - evidence[]
  - role_result.findings
  - boundaries[]
```

### media-processing

```yaml
maps_to:
  - artifacts.transcript
  - sources[]
  - evidence[]
  - boundaries[]
```

### knowledge-persistence

```yaml
maps_to:
  - artifacts
  - boundaries[]
```

写入私有知识库时，必须记录用户授权和目标路径。

## Failure Recovery

失败路径也必须回收：

```yaml
recovery:
  invocation_status: failed
  result_recovered: false
  recovered_as: []
  boundaries:
    - "peer skill 调用失败"
    - "未执行 fallback"
    - "没有伪造 sources 或 evidence"
```

## Final Output Integration

最终输出必须合并：

```text
结论
依据
角色观点
分歧与风险
行动建议
边界
```

peer skill 的结果不能绕过：

- quality gates
- role synthesis
- boundary statements
- capability status
