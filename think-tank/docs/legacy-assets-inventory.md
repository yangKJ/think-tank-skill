# Legacy Assets Inventory

本文记录旧 Claude Code 资产如何进入新的 think-tank 主仓。

这些旧资产是迁移素材，不是新体系中心。迁移时必须先抽象为 think-tank 协议、mode 或平台适配，再进入主仓。

## 旧资产来源

### research agent think-tank

路径：

```text
/Users/condy/Desktop/img-company/agents/research
```

关键资产：

- `.claude/skills/think-tank/SKILL.md`
- `.claude/skills/think-tank/skill.yaml`
- `.claude/skills/think-tank/README.md`
- `.claude/skills/think-tank/INTEGRATION.md`
- `.claude/agents/*.md`
- `.think-tank/conclusions/`
- `.think-tank/discuss-*/`
- `.claude/agent-memory/think-tank-issues-*.md`

可迁移价值：

- 多人协作触发词
- `simple-discuss`、`full`、`research-discuss` 工作流
- capability slots：`source_research`、`trend_analysis`、`synthesis`、`critic`
- agent documents 与 `subagent_type` 分离
- 调研、讨论、决策、执行的阶段意识
- 输出沉淀到 `.think-tank/conclusions/`
- Claude Code Agent Team 的平台约束记录

迁移位置：

- 触发和 mode 判断：`protocol/mode-selection.md`
- 角色和能力槽：`protocol/roles.md`
- research 场景：`modes/research.md`
- Claude Code 适配：`platforms/claude-code/`
- 示例：`examples/`

不要直接迁移：

- 旧 research 作为父级系统的结构
- 旧 `.claude` 私有目录假设
- 项目私有 agent 名称作为协议要求
- 未验证的 Agent Team 执行承诺

### agent-council

路径：

```text
/Users/condy/Desktop/ios-automation-mcp/.claude/skills/agent-council
```

关键资产：

- `SKILL.md`
- `references/agents.md`
- `references/scenes.md`
- `references/steps.md`
- `references/format.md`
- `references/state_contract.md`
- `scripts/state_manager.py`
- `scripts/research/*.py`
- `history/*`

可迁移价值：

- 主 Agent 作为纯主持人的边界
- 场景驱动选择 2 到 3 个最相关 Agent
- collect → discuss → conclude → complete 状态流
- 共享状态文件的状态契约
- L1/L2/L3 共识、调和、裁决机制
- discussion 文件格式和发言格式
- Feedback Synthesizer 汇总规则
- 失联、超时、重派、状态完整性等工程经验

迁移位置：

- council 场景：`modes/council.md`
- 动态角色选择：`protocol/roles.md`
- 讨论阶段：`protocol/think-tank-protocol.md`
- 质量门禁和裁决：`protocol/quality-gates.md`
- Claude Code 状态契约：`platforms/claude-code/`
- 示例：`examples/council-request.md`

不要直接迁移：

- `agent-council` 品牌作为平行主线
- ios-automation-mcp 项目私有上下文
- 旧 history 作为规范来源
- 旧脚本里的实现细节作为平台无关协议

## 统一归并原则

| 旧概念 | 新位置 |
|--------|--------|
| research think-tank | `modes/research.md` 和 Claude Code adapter |
| agent-council | `modes/council.md` 和 Claude Code adapter |
| capability slots | `protocol/roles.md` 的可配置能力层 |
| workflow trigger | `protocol/mode-selection.md` |
| collect/discuss/conclude | `protocol/think-tank-protocol.md` |
| state.json | `platforms/claude-code/runtime-contract.md` |
| Feedback Synthesizer | `protocol/roles.md` 的 `synthesizer` |
| L1/L2/L3 | `protocol/quality-gates.md` 和 `modes/council.md` |

## 第一批迁移目标

1. 将 research 触发词和 workflow 归并到 mode selection。
2. 将 capability slots 抽象为协议层角色和平台层 agent 映射。
3. 将 agent-council 的 collect/discuss/conclude 状态流写入 Claude Code runtime contract。
4. 将 L1/L2/L3 裁决机制抽象进 council mode。
5. 将旧平台约束写入 Claude Code adapter，避免误称为跨平台协议。

