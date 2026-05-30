# Architecture

think-tank 是一个跨平台、可复用的高阶 Skill，用于多角色信息收集、协作分析、讨论审议与结论汇总。

它的核心不是某个平台的脚本，也不是某个领域的 agent，而是一套可以被不同平台执行的协议和能力编排模型。

## 总体结构

```text
think-tank
├── protocol/       # 唯一协议源
├── modes/          # 场景模式
├── profiles/       # 跨平台角色模板
├── capabilities/   # 外部能力槽
├── platforms/      # 平台适配
├── schemas/        # 机器可读输入输出契约
├── examples/       # 示例
└── docs/           # 架构、迁移、使用说明
```

## 核心分层

### protocol

`protocol/` 是唯一真相源。

它定义：

- 触发条件
- 输入输出
- mode 选择
- 角色选择
- 流程阶段
- 质量门禁
- 版本演进

任何平台和领域都不能改写协议层语义。

### modes

`modes/` 定义任务场景。

第一批 mode：

- `research`：研究、资料收集、证据整理
- `council`：多角色审议、观点碰撞、决策
- `review`：审查、验收、问题发现
- `strategy`：路线、产品、架构和优先级

mode 只定义场景默认策略，不能变成平行产品。

### profiles

`profiles/` 定义跨平台角色模板。

profile 不是 Claude Code subagent，也不是 Codex agent。它是平台无关的角色能力定义。

示例：

- `source-collector`
- `trend-analyst`
- `social-listener`
- `feedback-synthesizer`
- `report-architect`
- `skeptic`
- `product-strategist`
- `facilitator`

平台 adapter 可以把 profile 映射成真实 subagent、单 agent 分段执行、脚本或人工步骤。

### capabilities

`capabilities/` 定义外部能力槽。

think-tank 不复制工具型 skill。它通过 capability 说明“需要什么能力”，再由平台 adapter 调用当前可用工具。

示例：

- `source-acquisition`
- `media-processing`
- `media-production`
- `social-listening`
- `knowledge-persistence`
- `browser-automation`

`yt-dlp`、`obsidian`、`playwright-cli`、`xiaohongshu` 等都属于能力实现候选，不属于 think-tank core。

### platforms

`platforms/` 定义不同运行环境如何执行 think-tank。

当前平台：

- `claude-code`
- `codex`

平台允许不同：

- subagent 调用方式
- 工具和 skill 调用方式
- 文件落点
- 记忆策略
- runtime 限制

平台不允许不同：

- 协议阶段
- mode 语义
- profile 职责
- 输出结构
- 质量门禁

### domain-packs

`domain-packs/` 已迁至 `.think-tank/domain-packs/`（本地配置，不随公开 Skill 发布）。

领域包可以提供：

- 默认竞品
- 技术雷达
- 默认信息源
- 领域报告模板
- 监控关键词

领域包不能改变 think-tank 协议。

私有领域经验不进入当前主仓。需要领域知识的项目应在自己的仓库中维护 domain pack 或本地资料。

## 旧系统迁移关系

```text
旧 research agent
├── skills 工具链          -> capabilities + Claude Code skill mapping
├── subagents             -> profiles + Claude Code agent mapping
├── 私有领域知识           -> 项目本地 domain pack / 本地资料
└── think-tank 协作原型    -> protocol + research/council modes

旧 agent-council
├── 多角色审议流程         -> council mode
├── collect/discuss/conclude -> protocol stages + Claude Code runtime contract
├── L1/L2/L3 裁决          -> council mode + quality gates
└── state.json 工程实现    -> Claude Code runtime contract
```

## 执行路径

标准执行路径：

```text
用户任务
  -> mode selection
  -> profile selection
  -> capability selection
  -> platform adapter execution
  -> role outputs
  -> deliberation / synthesis
  -> quality gates
  -> final output
```

## 与领导者运行层的关系

在基础执行路径之上，主 agent 的领导者编排层已经从 `think-tank/` 中拆出，迁移到外部 sibling 项目 `leader-runtime-project`。

`think-tank/` 不再承担以下主语：

- 主 agent 如何升级为领导者
- 如何维护全量专家池
- 如何向项目派生领导者下放子集专家编制
- 如何做真实派遣、结果回收、验收和仲裁

这些内容改由外部 sibling 项目文档定义：

```text
Desktop/leader-runtime-project/docs/codex-leader-orchestration-blueprint.md
```

think-tank 在领导者体系中的定位，是被调用的高阶 Skill core。

## Codex 执行边界

Codex 当前可以验证：

- 协议可读
- mode/profile/capability 可选择
- 单 agent 多 profile 模拟执行
- 本地仓库证据收集
- 结构化输出
- 质量门禁

Codex 当前不能证明：

- Claude Code Agent Team 已完成
- 旧 `.claude/skills` 可被直接调用
- 真实多 agent 并发已完成
- 外部工具型 skill 都已集成

## Claude Code 执行边界

Claude Code adapter 的目标是：

- 映射 profiles 到 `.claude/agents`
- 映射 capabilities 到 `.claude/skills`
- 管理 Agent Team 或 subagent 生命周期
- 回收结果
- 标注 verified/mock/tracking/planned

在真实执行和结果回收前，不能把 Claude Code 路径标为 verified。
