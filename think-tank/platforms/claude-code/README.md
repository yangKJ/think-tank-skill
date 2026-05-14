# Claude Code Adapter

该目录定义 think-tank 在 Claude Code 中的适配方式。

## 职责

- 把 `protocol/` 映射为 Claude Code 可执行的 Skill 行为
- 定义如何调用 Claude Code agent、subagent 或替代执行单元
- 定义中间结果和最终结果的保存方式
- 定义失败恢复和结果回收机制
- 明确哪些路径已真实验证，哪些只是 mock 或 tracking

## 初始约束

旧 research 体系中的 think-tank 资产可以迁入本适配，但迁入后必须服从主协议。

旧实现中如果存在 mock 路径、tracking-only 路径或未完成的真实 Team 执行路径，必须明确标注，不能作为主协议已完成能力宣传。

## 后续文件规划

- `adapter.md`：Claude Code 适配协议
- `dispatch-contract.md`：capability 到 skill/tool 的最小 dispatch 契约
- `dispatch-prompt.md`：Claude Code dispatch 验证标准提示词
- `final-validation-prompt.md`：Claude Code 最终低流量验证提示词
- `minimal-runtime.md`：Claude Code 最小 adapter runtime 约定
- `runtime-contract.md`：真实执行、结果回收和失败恢复约定
- `skill-mapping.md`：Claude Code skills 到 think-tank capabilities 的映射
- `agent-mapping.md`：Claude Code subagents 到 think-tank profiles 的映射
- `migration-notes.md`：从旧 research think-tank 迁入的资产清单
