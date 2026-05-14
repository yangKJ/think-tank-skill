# Usage

本文说明如何使用 think-tank 主 Skill。

## 基本入口

Skill 本体入口是：

```text
think-tank/SKILL.md
```

协议入口是：

```text
think-tank/protocol/think-tank-protocol.md
```

## 使用步骤

1. 读取用户任务。
2. 根据 `protocol/mode-selection.md` 选择 mode。
3. 根据 `protocol/agent-selection.md` 和 `profiles/` 选择角色模板。
4. 根据 `capabilities/` 选择需要的外部能力。
5. 根据平台 adapter 决定如何调用 skills、subagents 或工具。
6. 按协议阶段执行：收集、分析、讨论、汇总、建议。
7. 通过 `protocol/quality-gates.md` 检查输出。

## Mode 快速选择

| 用户目标 | mode |
|----------|------|
| 研究资料、对比证据、形成调研结论 | `research` |
| 多角色讨论、观点碰撞、做决策 | `council` |
| 审查代码、方案、文档或产出 | `review` |
| 产品、架构、路线和优先级规划 | `strategy` |

## Claude Code

Claude Code 的适配说明：

```text
think-tank/platforms/claude-code/adapter.md
think-tank/platforms/claude-code/runtime-contract.md
```

旧 research think-tank 和 agent-council 都属于 Claude Code 旧资产来源，迁移时必须区分平台实现和主协议。

## Codex

Codex 的适配说明：

```text
think-tank/platforms/codex/adapter.md
```

当前 Codex 默认采用单 agent 协议执行，可以模拟多角色分析，但不能把模拟说成真实多 agent 协作。

## 外部 skills 共存

think-tank 不复制工具型 skill。它通过 `capabilities/` 声明能力槽，由平台 adapter 调用当前环境可用的 skills。

例如：

- 视频任务：`media-processing` 可映射到 `yt-dlp`、`openai-whisper`、`summarize`
- 社媒任务：`social-listening` 可映射到 `xiaohongshu`、`social-media-analyzer`
- 知识沉淀：`knowledge-persistence` 可映射到 `obsidian`、`notebooklm`

无论外部 skill 输出什么，最终都必须回到 think-tank 的协议输出结构。
