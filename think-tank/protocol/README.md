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
- `intent-routing.md`：平台无关自然语言触发、intent 和 recipe 路由规则
- `skill-trigger-intelligence.md`：3.0 skill 使用判断协议，明确 trigger examples 属于用户 YAML policy 而不是 core 内置规则
- `skill-invocation-contract.md`：3.0 agent 调用 think-tank 前后的输入输出契约
- `progressive-disclosure.md`：3.0 渐进式加载规则，避免 agent 一次性加载整个仓库
- `roles.md`：角色职责、选择规则和角色输出契约
- `agent-selection.md`：场景驱动的角色和平台 agent 选择规则
- `mode-selection.md`：场景模式选择规则
- `quality-gates.md`：质量门禁和验收标准
- `artifact-quality-gates.md`：生成物、媒体成品、报告、样例和 run record 的成品验收门禁
- `runtime-contract.md`：平台无关 runtime pipeline
- `natural-language-runtime-orchestration.md`：自然语言请求到 policy、dispatch、invocation、recovery、run record 的最小闭环
- `state-result-contract.md`：run、state、result、recovery 最小结构
- `minimal-conclusion-contract.md`：跨 mode 的最小结论收口契约，统一 request、route、decision、evidence、risk 和 next_step
- `consensus-contract.md`：显式投票、blocking objection、停止条件
- `runtime-provenance.md`：运行来源披露门禁，防止把直接工具调用或单 agent 模拟写成真实 runtime
- `run-record.md`：2.0 可回放运行记录协议
- `project-memory-runtime.md`：2.0 项目记忆运行时，定义 episodic、semantic、procedural memory 和冲突处理
- `provider-invocation-ledger.md`：2.0 provider 调用证据账本，区分 selected、preflight、invoked、recovered 和 verified
- `handoff-protocol.md`：2.0 profile、subagent、provider 和 human handoff 契约
- `guardrails.md`：2.0 权限、隐私、证据、artifact、memory 和 security gate
- `research-os.md`：2.0 本地 `.think-tank/` Research OS 工作区契约
- `eval-pack.md`：2.0 协议回归评测包
- `capability-evidence-state-machine.md`：capability 证据状态机
- `evidence-sources.md`：统一证据来源表，区分本地代码、文档、网页、用户材料、推理和缺失数据
- `artifact-write-policy.md`：报告、运行记录、backlog 和项目文档的写入策略
- `strategy-to-backlog.md`：把策略建议转成可验收 backlog 候选的结构
- `post-run-curation.md`：研究、趋势、策略、审查和内容规划任务结束后的来源候选、趋势候选、行动候选、artifact plan 和持久化决策协议
- `memory-curation.md`：项目记忆候选生成协议
- `memory-promotion-policy.md`：项目记忆提升到 AGENTS、项目文档或公开协议的规则
- `versioning.md`：协议版本演进和能力状态标注规则

与外部 peer skills 的连接规则放在 `routing/`。它不是协议真相源，但负责把协议层的 capability slots 转成可执行的 skill route、dispatch decision 和 result recovery。
