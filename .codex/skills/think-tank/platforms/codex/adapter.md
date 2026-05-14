# Codex Adapter

本文定义 think-tank 在 Codex 中的适配方式。

Codex 是执行环境，不是协议源。Codex adapter 必须遵守 `protocol/`，只能决定如何执行、记录和验证 think-tank。

## 能力状态

```yaml
adapter: codex
adapter_version: 0.1.0
status:
  single_agent_protocol_execution: verified
  local_repository_collection: verified
  tool_assisted_verification: verified
  parallel_subagent_execution: planned
  persistent_think_tank_memory: planned
```

## 执行模型

Codex 初始采用单 agent 协议执行：

1. 读取用户请求。
2. 根据 `protocol/mode-selection.md` 选择 mode。
3. 根据 `protocol/roles.md` 选择角色。
4. 使用本地文件、shell、浏览器或其他可用工具收集证据。
5. 依次模拟角色独立分析。
6. 汇总角色分歧和共识。
7. 执行 `protocol/quality-gates.md`。
8. 输出结论、依据、分歧、风险和行动建议。

当用户明确要求并行 agent，且当前环境支持 subagent 时，可以把角色拆给 subagent；否则必须明确这是单 agent 执行。

## Codex 工具使用

Codex adapter 可以使用：

- 文件读取和编辑
- `rg`、`find`、`git status` 等本地命令
- 项目测试命令
- 浏览器或联网工具，前提是任务允许
- Codex subagent，前提是用户明确要求或平台允许

使用工具时必须遵守任务上下文和权限边界。

## 记忆和上下文

Codex adapter 可以读取可用的本地项目记忆，但必须区分：

- 当前仓库事实
- 旧记忆
- 用户本轮指令
- 推断

当记忆和当前仓库冲突时，以当前仓库和用户最新指令为准。

## 输出要求

Codex 输出应保持中文优先，除非用户或项目文件明确要求英文。

标准输出至少包含：

- 结论
- 依据
- 分歧与风险
- 行动建议
- 边界

代码修改类任务还应说明：

- 修改了哪些文件
- 是否运行验证
- 验证结果
- 未验证的风险

## 禁止行为

- 不把 Codex 的工具限制写成 think-tank 协议限制。
- 不把单 agent 模拟说成真实多 agent 协作。
- 不把未运行的测试说成已验证。
- 不把旧记忆当成当前事实。

