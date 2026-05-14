# Capability Degradation: Knowledge Persistence

## 测试任务

```text
用户要求把 think-tank 讨论结论保存到知识库；当前不调用 obsidian、notebooklm 或 taskflow。
```

## 执行声明

```yaml
platform: codex
mode: research
capability: knowledge-persistence
external_skills:
  obsidian: unavailable
  notebooklm: unavailable
  taskflow: unavailable
execution_method: local_markdown_artifact
```

## 降级执行

由于没有调用外部知识库工具，think-tank 不写用户私有 Obsidian vault，也不声称已经创建 NotebookLM 或持久任务流。

可执行降级路径：

1. 在当前仓库写入 Markdown artifact。
2. 标注 artifact 位置。
3. 如果用户之后指定知识库路径或工具，再由平台 adapter 执行迁移。

## 可输出结果

```yaml
saved: true
location: "think-tank/examples/or/docs 下的 Markdown 文件"
artifact_type: report
follow_up:
  - 如需写入 Obsidian，需要用户明确目标 vault 或授权路径
```

## 验证结论

knowledge-persistence capability 可以在外部知识库工具不可用时降级为本地 Markdown artifact。该路径已在 Codex 中验证，因为当前验证报告和示例均写入仓库文件。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

