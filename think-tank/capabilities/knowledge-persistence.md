# Knowledge Persistence

## 目的

将 think-tank 的研究、讨论、证据和结论沉淀为可复用知识。

## 适用场景

- 研究报告需要长期保存
- 讨论结论需要后续追踪
- 需要避免重复研究
- 需要建立知识图谱或笔记体系

## 输入

```yaml
artifact_type: brief | report | evidence_table | decision_memo | monitoring_log | knowledge_graph
title: ""
content: ""
tags: []
target: ""
```

## 输出

```yaml
saved: true
location: ""
artifact_type: ""
follow_up: []
```

## 候选 skills

- `obsidian`
- `notebooklm`
- `knowledge-graph-builder`
- `taskflow`

## 降级策略

- 没有知识库工具时，输出 Markdown artifact。
- 目标路径不明确时，不硬编码用户私有路径。
- 持续监控类任务应记录状态和下一次检查条件。

