# Codex Local Source Artifact

本文是 Codex 主平台 `source-acquisition + knowledge-persistence` 的本地资料沉淀样例。

## Artifact Metadata

```yaml
platform: codex
artifact_type: decision_memo
mode: research
capabilities:
  - source-acquisition
  - knowledge-persistence
source_scope: local_repository
external_skills_invoked: false
status: verified
```

## 主题

Codex 作为 think-tank 主平台时，最低依赖的日常闭环是什么？

## 结论

Codex 的最低依赖日常闭环应是：

```text
用户任务
  -> mode/profile/capability 选择
  -> 本地资料和用户材料读取
  -> 多 profile 分段判断
  -> 结构化输出
  -> Markdown artifact 沉淀
  -> checks 验收
```

这条路径不依赖 Claude Code、不依赖 Browser、不依赖 Obsidian、不依赖社媒或媒体处理工具。

## 本地来源

| 来源 | 用途 | 可靠性 |
|------|------|--------|
| `think-tank/SKILL.md` | Skill 入口和执行顺序 | high |
| `think-tank/platforms/codex/operating-guide.md` | Codex 主平台运行方式 | high |
| `think-tank/platforms/codex/capability-status.md` | capability 状态边界 | high |
| `think-tank/docs/minimal-install-behavior.md` | 最小安装能力边界 | high |
| `think-tank/docs/codex-acceptance.md` | Codex 验收标准 | high |

## 角色观点

```yaml
source_collector:
  claim: 本地仓库已经包含足够的协议、平台和验证材料，可支持 Codex 日常运行。
  evidence:
    - think-tank/SKILL.md
    - think-tank/platforms/codex/operating-guide.md
  confidence: high

skeptic:
  claim: 这条路径不能证明外部网页浏览、真实多 agent 或 Claude Code runtime。
  evidence:
    - think-tank/docs/codex-acceptance.md
    - think-tank/platforms/codex/capability-status.md
  confidence: high

report_architect:
  claim: Markdown artifact 是 knowledge-persistence 的安全降级实现，适合公开仓库和跨平台复用。
  evidence:
    - think-tank/capabilities/knowledge-persistence.md
  confidence: high
```

## 风险

- 本地资料闭环如果不要求 checks，容易变成普通文档堆积。
- Markdown artifact 不能替代 Obsidian、NotebookLM 或知识图谱能力。
- 如果 artifact 不记录来源和边界，后续迁移到 Claude Code 时容易误判状态。

## 行动建议

1. Codex 日常任务默认优先使用本地资料和用户材料。
2. 每个可复用结论沉淀为 Markdown artifact。
3. artifact 必须写明 `platform`、`capabilities`、`source_scope`、`external_skills_invoked` 和 `status`。
4. 验证类 artifact 必须纳入 `checks/codex_validation_check.py` 或相关检查脚本。
5. 外部能力仅在本地闭环不能满足任务时启用。

## 边界

本 artifact 没有联网，没有打开 Browser，没有写入私有知识库，没有调用 Claude Code subagent。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

