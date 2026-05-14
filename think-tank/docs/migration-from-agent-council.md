# Migration from Agent Council

agent-council 是 think-tank 的历史实现分支，主要价值在于多角色讨论、状态机驱动、裁决机制和结果汇总。

在新体系中，agent-council 应被收编为 `council mode`，不再作为平行主线。

## 来源路径

```text
/Users/condy/Desktop/ios-automation-mcp/.claude/skills/agent-council
```

## 应保留的设计

### 主 Agent 纯主持人

旧 agent-council 的一个重要边界是：

> 主 Agent 只协调流程，不发表技术观点。

新体系应保留为 council mode 的默认原则：

- 主 Agent 负责议题、派发、轮次、汇总。
- 专业角色负责观点。
- 主 Agent 只有在 L3 裁决时才给出裁决。

### 三阶段流程

旧流程：

```text
collect -> discuss -> conclude -> complete
```

新体系映射到主协议：

| agent-council 阶段 | think-tank 阶段 |
|--------------------|-----------------|
| collect | `collection` |
| discuss | `deliberation` |
| conclude | `synthesis` + `recommendation` |
| complete | `quality_check` 后结束 |

### L1/L2/L3 机制

旧机制：

- L1：达到共识，自动进入汇总
- L2：未充分共识，继续调和
- L3：超时、轮次上限或低共识时裁决

新体系应放入：

- `modes/council.md`
- `protocol/quality-gates.md`
- `platforms/claude-code/runtime-contract.md`

### 场景驱动 Agent 选择

旧体系按关键词选择 2 到 3 个最相关 Agent。

新体系应抽象为：

- protocol 层：动态角色选择规则
- mode 层：council 默认角色组合
- platform 层：Claude Code 的具体 agent display name 映射

## 应降级为平台细节的内容

以下内容不应进入平台无关协议：

- `state.json` 具体字段
- HMAC 签名实现
- 文件权限 `700` / `600`
- manifest 签名
- Python 状态机脚本
- ios-automation-mcp 历史案例路径

这些内容可以进入 Claude Code adapter 的 runtime contract，作为该平台的工程实现经验。

## 迁移步骤

1. 将“纯主持人”写入 `modes/council.md`。
2. 将 collect/discuss/conclude/complete 写入 Claude Code runtime contract。
3. 将 L1/L2/L3 机制抽象到 council mode 与质量门禁。
4. 将动态 Agent 选择规则合并到 `protocol/roles.md`。
5. 将讨论文档格式转成 `examples/council-request.md` 或新的 council 输出模板。
6. 将状态机脚本暂列为 Claude Code 适配候选实现，不直接进入主协议。

