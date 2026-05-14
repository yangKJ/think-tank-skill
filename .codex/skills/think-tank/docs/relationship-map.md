# Relationship Map

## 主关系

```text
think-tank
├── protocol: 唯一主协议
├── platforms: Claude Code / Codex / future adapters
└── modes
    ├── research: 原 research 体系的研究用法
    ├── council: agent-council 的多角色审议能力
    ├── review: 审查和验收能力
    └── strategy: 策略和路线能力
```

## research

research 在新体系中是 think-tank 的核心应用场景之一。它负责研究、资料收集、证据整理和结论输出。

research 不再是 think-tank 的父级，不应拥有高于 think-tank 协议层的行为定义权。

## agent-council

agent-council 在新体系中是 think-tank 的历史实现分支或 council mode 来源。它的价值在于多角色讨论、交叉质询、冲突暴露和审议收敛。

agent-council 不应继续作为独立主线平行发展。可复用资产应迁入 `modes/council.md`、`protocol/` 或对应平台适配。

## Claude Code 旧资产

research think-tank 和 agent-council 当前都来自 Claude Code 平台。迁移时应先判断资产性质：

- 平台无关行为：进入 `protocol/`
- 场景默认策略：进入 `modes/`
- Claude Code 执行细节：进入 `platforms/claude-code/`
- 历史案例和运行产物：进入 `examples/` 或迁移文档

## 平台

Claude Code 和 Codex 都是 think-tank 的执行环境，不是协议源。

平台可以决定如何执行，但不能决定 think-tank 是什么。
