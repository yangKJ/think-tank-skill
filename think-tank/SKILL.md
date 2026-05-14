# think-tank Skill

## 定位

think-tank 是一个跨平台、可复用的高阶 Skill，用于多角色信息收集、协作分析、讨论审议与结论汇总。

它不是工具合集，不复制外部 skills；它负责任务理解、协议执行、角色组织、能力编排和最终汇总。

## 何时使用

当用户任务满足任一条件时，使用 think-tank：

- 需要多渠道信息收集
- 需要多个角色分别判断
- 需要讨论、审议、观点碰撞或决策
- 需要审查产物、发现问题或验收
- 需要策略、路线、产品或架构判断
- 需要把复杂资料汇总为行动建议

旧 research agent 风格触发词也应进入 think-tank：

- `研究一下`、`帮我了解一下`、`行业分析`
- `深度研究`、`全面研究`、`系统分析`
- `竞品分析`、`竞品动态`
- `舆情分析`、`小红书用户评价`
- `开会讨论`、`讨论一下`

Codex 平台的详细触发路由见：

```text
platforms/codex/trigger-routing.md
```

不应强行使用 think-tank：

- 简单事实查询
- 单页摘要
- 明确的一步命令
- 不需要多角色或证据判断的任务

## 执行顺序

### 1. 解析任务

提取：

- 用户目标
- 已知上下文
- 约束
- 成功标准
- 是否需要实时信息
- 期望输出

### 2. 选择 mode

按 `protocol/mode-selection.md` 选择：

- `research`：研究、信息收集、证据整理
- `council`：多角色讨论、审议、决策
- `review`：审查、验收、问题发现
- `strategy`：路线、产品、架构和优先级

如果无法判断，默认使用 `council`，并说明原因。

### 3. 选择 profiles

按 `profiles/` 和 `protocol/agent-selection.md` 选择角色模板。

常用 profiles：

- `facilitator`
- `source-collector`
- `trend-analyst`
- `social-listener`
- `feedback-synthesizer`
- `report-architect`
- `skeptic`
- `product-strategist`

选择角色时不要固定凑人数。角色必须服务任务。

### 4. 选择 capabilities

按 `capabilities/` 选择需要的外部能力槽：

- `source-acquisition`
- `media-processing`
- `social-listening`
- `knowledge-persistence`
- `browser-automation`

capability 不是具体工具。平台 adapter 负责把 capability 映射成当前可用的 skills、工具或执行步骤。

如果当前平台是 Claude Code，并且任务需要调用外部 skill/tool，必须遵守：

```text
platforms/claude-code/dispatch-contract.md
```

也就是说，在调用外部 skill/tool 前必须形成 `dispatch_decision`，调用后必须形成 `dispatch_log`，并将结果回收到 `sources[]`、`evidence[]` 或对应输出结构。

### 5. 平台执行

根据当前平台执行：

- Codex：优先遵守 `platforms/codex/specialist-subagent-runtime.md`。如果当前环境没有已验证的独立 subagent runtime，必须标记为 `single_agent_multi_profile_fallback`，不能声称独立专家执行。
- Claude Code：可映射到 `.claude/agents`、`.claude/skills`、Agent Team 或 subagent；涉及 capability 到 skill/tool 的调用时，必须输出 `dispatch_request`、`dispatch_decision`、`dispatch_log`；涉及专业 subagent 时，必须遵守 `platforms/claude-code/specialist-subagent-runtime.md` 并回收 `role-result`。
- 其他平台：遵守协议，按自身能力实现。

平台差异必须标注，不得改变主协议。

专业 subagent 输出必须符合：

```text
schemas/role-result.schema.json
```

如果只是在同一上下文里扮演多个 profile，最终输出必须说明：

```yaml
execution_method: single_agent_multi_profile_fallback
authority_level: lower_fallback_single_context
```

### 6. 汇总输出

最终输出必须回到 think-tank 结构：

```text
结论
依据
角色观点
分歧与风险
行动建议
边界
```

轻量任务可以合并栏目，但不能丢失结论、风险和行动建议。

### 7. 质量检查

输出前检查：

- 是否明确 mode
- 是否说明角色或视角
- 是否区分事实、推断和建议
- 是否列出分歧或风险
- 是否给出可执行下一步
- 是否说明未验证或受限部分
- 是否没有把 mock/tracking/planned 说成 verified
- 是否没有把 single-agent fallback 说成 specialist subagent runtime

## 外部 skills 共存规则

think-tank 可以编排外部 skills，但不拥有它们。

示例映射：

- 视频研究：`media-processing` -> `yt-dlp`、`openai-whisper`、`summarize`
- 社媒舆情：`social-listening` -> `xiaohongshu`、`social-media-analyzer`
- 知识沉淀：`knowledge-persistence` -> `obsidian`、`notebooklm`
- 浏览器任务：`browser-automation` -> `web-access`、`playwright-cli`

如果外部 skill 不可用，按 capability 的降级策略处理，并在边界中说明。

## 旧资产关系

- 旧 research agent 是 research mode、capabilities、profiles 和 Claude Code 映射的来源材料。
- 旧 agent-council 是 council mode 和 Claude Code runtime contract 的来源材料。
- 图像编辑 App 经验属于 `domain-packs/image-editing/`，不是 core。

## 能力状态

任何平台能力都必须标注：

- `verified`：真实执行并验证
- `mock`：只在模拟路径验证
- `tracking`：只记录状态，不代表执行完成
- `planned`：设计目标，尚未实现

## 入口文档

- 架构总览：`docs/architecture.md`
- 核心协议：`protocol/think-tank-protocol.md`
- mode 选择：`protocol/mode-selection.md`
- profiles：`profiles/`
- profile prompt pack：`profiles/prompt-pack.md`
- capabilities：`capabilities/`
- 平台适配：`platforms/`
