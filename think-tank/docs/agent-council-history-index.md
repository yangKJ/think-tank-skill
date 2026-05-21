# Agent Council History Index

本文记录旧 agent-council `history/` 目录的处置方式。

## 结论

```yaml
history_disposition: indexed_not_copied
history_as_protocol_truth_source: false
ios_automation_context_imported: false
```

旧 history 包含 agent selection、workflow optimization、self healing、state manager tests、多次 v7.x 讨论和具体项目案例。它们是历史样例，不是新 think-tank 协议真相源。

## 历史项处置

| 旧 history 项 | 处置 |
|---------------|------|
| `agent_selection_review.md` | 进入 agent selection 经验 |
| `auto_execution_test/` | 状态机自动执行样例，进入 runtime migration |
| `collab_review.md` | council mode 协作经验 |
| `collab_skill_review.md` | legacy inventory 经验 |
| `collect-cr.md` | collect 阶段样例 |
| `council_v2_issues_review*` | issue 经验，进入 runtime boundaries |
| `council_v77_review.md` | v7.7 状态机经验 |
| `council_v791_review.md` | v7.9.1 安全经验 |
| `council_workflow_optimization.md` | workflow optimization 经验 |
| `doc_location_review.md` | 文档落点经验 |
| `project-codex-sample/` | 项目私有样例，不迁入 |
| `project-prompt-sample/` | 项目私有样例，不迁入 |
| `multi_agent_research_design/` | research 子系统设计经验 |
| `self_healing_review/` | retry / skipped / circuit breaker 经验 |
| `skill-review.md` | skill 审查经验 |
| `skill_naming_review.md` | 命名经验 |
| `v76_test/`、`v78_test.md` | 状态机测试经验 |

## 使用边界

- 可以作为未来 regression scenario 的素材。
- 不把旧 history 原文复制成当前规范。
- 不带入项目私有目标。
- 不把旧脚本测试通过当成 think-tank 当前 runtime 已验证。
