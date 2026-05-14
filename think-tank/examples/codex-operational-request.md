# Codex Operational Request

本文件给出 Codex 主平台日常使用 think-tank 的请求示例。

## 请求

```text
用 think-tank council mode 讨论：

议题：
Codex 作为 think-tank 的主平台时，下一步应该优先验证外部网页只读 Browser，还是先完善本地 source-acquisition 和 Markdown artifact？

约束：
- 不切到 Claude Code。
- 不安装高风险外部 skill。
- 不把 optional capability 说成 core dependency。

最终输出：
- 共识
- 分歧
- 推荐路线
- 下一步行动
```

## 预期选择

```yaml
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
execution_method: codex_single_agent_multi_profile
```

## 预期输出边界

```yaml
must_include:
  - 不声称真实多 agent
  - 不声称 Browser 外部网页已验证
  - 不声称 Obsidian 或 Playwright 已集成
  - 给出 Codex 内可执行下一步
```

