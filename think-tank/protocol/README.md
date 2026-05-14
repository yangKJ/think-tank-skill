# protocol

`protocol/` 是 think-tank 的协议层，也是本仓库最重要的唯一真相源。

这里的内容必须平台无关，不能写死 Claude Code、Codex 或任何单一项目的实现细节。

## 本层负责

- 触发条件
- 输入格式
- 角色选择机制
- 流程阶段
- 收集、分析、讨论、汇总、输出的顺序
- 终止条件
- 输出结构
- 质量判断标准
- 协议版本演进规则

## 本层不负责

- 平台如何调用 subagent
- 运行时脚本如何组织
- 记忆或缓存落在哪个目录
- hook 如何接入
- 某个项目的专用上下文

这些内容应放在 `platforms/` 或具体项目适配中。

## 文件

- `think-tank-protocol.md`：核心协议正文
- `input-output.md`：输入输出契约
- `roles.md`：角色职责、选择规则和角色输出契约
- `agent-selection.md`：场景驱动的角色和平台 agent 选择规则
- `mode-selection.md`：场景模式选择规则
- `quality-gates.md`：质量门禁和验收标准
- `runtime-contract.md`：平台无关 runtime pipeline
- `state-result-contract.md`：run、state、result、recovery 最小结构
- `consensus-contract.md`：显式投票、blocking objection、停止条件
- `versioning.md`：协议版本演进和能力状态标注规则
