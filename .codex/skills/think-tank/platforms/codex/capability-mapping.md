# Codex Capability Mapping

本文定义 think-tank capabilities 在 Codex 平台上的初始映射。

Codex 当前以单 agent 多 profile 模拟执行为默认路径。它可以使用本地文件、shell、浏览器、联网工具和可用插件，但不能把模拟执行说成真实多 agent 协作。

## 能力状态

```yaml
adapter: codex
capability_mapping_version: 0.1.0
status:
  single_agent_profile_simulation: verified
  local_repository_collection: verified
  shell_verification: verified
  browser_or_web_access: environment_dependent
  external_skill_invocation: planned
  true_multi_agent_execution: planned
  external_research_skills_installed: verified
```

## 映射表

| capability | Codex 初始实现 |
|------------|----------------|
| `source-acquisition` | 读取本地文件、`rg`、shell、必要时 web 搜索 |
| `browser-automation` | Codex Browser / Playwright 能力，视环境可用性 |
| `media-processing` | 当前为 planned；可在有工具时调用本地 CLI |
| `social-listening` | 当前为 planned；可用 web 或用户提供样本降级 |
| `knowledge-persistence` | 写入仓库文档、Markdown artifact；不默认写用户私有知识库 |

旧 research agent 的工具型 skills 已按同级关系安装到 Codex skills 目录。think-tank 可以把它们视为 optional peer skill 候选实现，但必须通过 `routing/skill-router.md` 和 `routing/dispatch-policy.md` 逐次选择和验证执行能力。

## 执行方式

Codex 执行 think-tank 时：

1. 读取 `SKILL.md` 和相关协议文件。
2. 根据用户任务选择 intent、recipe 和 mode。
3. 选择 profiles 和 capabilities。
4. 用 routing 层形成 skill_route 和 dispatch_decision。
5. 用 Codex 工具或 optional peer skills 收集本地或外部证据。
6. 按 result-recovery 回收到 sources、evidence、artifacts 或 boundaries。
7. 汇总角色观点、分歧、风险和行动建议。
8. 运行必要检查。
9. 明确哪些能力是 verified，哪些只是 planned。

## 降级规则

- 不能调用外部 skill 时，使用本地资料或用户提供资料。
- 不能联网时，标注信息边界。
- 不能真实并行 subagent 时，使用单 agent 分段模拟，并明确声明。
- 不写用户私有知识库，除非用户明确要求。
