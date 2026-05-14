# Codex Operational Validation

本文件记录 Codex 主平台日常使用场景的验证。

## 测试任务

```text
用 think-tank council mode 讨论：

议题：
Codex 作为 think-tank 的主平台时，下一步应该优先验证外部网页只读 Browser，还是先完善本地 source-acquisition 和 Markdown artifact？

约束：
- 不切到 Claude Code。
- 不安装高风险外部 skill。
- 不把 optional capability 说成 core dependency。
```

## 执行声明

```yaml
platform: codex
execution_method: single_agent_multi_profile
mode: council
profiles:
  - facilitator
  - product-strategist
  - skeptic
  - report-architect
capabilities:
  - source-acquisition
  - browser-automation
  - knowledge-persistence
verified:
  - codex_operational_template_execution
  - mode_selection
  - profile_selection
  - capability_boundary_declaration
  - actionable_recommendation
not_verified:
  - external_web_browser_execution
  - obsidian_write
  - true_multi_agent_discussion
```

## 结论

下一步应优先完善本地 `source-acquisition` 和仓库内 Markdown artifact 路径，然后再做外部网页只读 Browser 测试。

理由：

1. 本地 source-acquisition 和 Markdown artifact 是 Codex 主平台日常使用的最低价值路径。
2. Browser 已完成 localhost fixture 的 optional 验证，继续外部网页只读测试有价值，但不应抢在基础运行体验之前。
3. 完善本地路径可以服务 research、review、strategy 和 council 四个 mode，而外部网页 Browser 主要增强 source acquisition。

## 角色观点

```yaml
facilitator:
  claim: 当前议题不是是否需要 Browser，而是 Codex 主平台的下一步优先级。
  recommendation: 先把最低依赖路径做成稳定日常流程。
  confidence: high

product_strategist:
  claim: 用户当前主要平台是 Codex，因此最重要的是让 Codex 下的普通任务可持续复用。
  recommendation: 优先沉淀任务模板、capability 状态和本地 artifact 规范。
  confidence: high

skeptic:
  claim: 如果继续验证 Browser 外部网页，容易让人误解为 think-tank 依赖 Browser。
  recommendation: Browser 继续保持 optional，并且每次验证都写清边界。
  confidence: high

report_architect:
  claim: 本地 source-acquisition 和 Markdown artifact 更适合形成可检查、可迁移、可发布的 foundation。
  recommendation: 将 Codex 日常运行手册、任务模板和 capability 状态矩阵纳入验收。
  confidence: high
```

## 分歧与风险

- 分歧：Browser 外部网页只读测试是否应该马上做。
- 判断：可以做，但不应成为下一步主线；主线应先服务 Codex 日常使用。
- 风险：Codex 主平台文档过多，用户不知道入口。
- 缓解：入口集中到 `platforms/codex/operating-guide.md`、`task-templates.md` 和 `capability-status.md`。

## 行动建议

1. 将 Codex 主平台运行手册纳入验收。
2. 将任务模板作为日常触发入口。
3. 将 capability 状态矩阵作为是否调用外部能力的判断依据。
4. 下一轮再选择 `source-acquisition + Markdown artifact` 做一个真实任务样例。
5. Browser 外部网页只读测试保留为后续 optional capability 验证。

## 边界

本次没有打开外部网页，没有写入 Obsidian，没有调用 Playwright，也没有执行真实多 agent。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```
