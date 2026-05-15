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

通用触发词也应进入 think-tank：

- 研究：`研究一下`、`帮我了解一下`、`深度研究`、`全面分析`
- 竞争：`竞品分析`、`竞争分析`、`对比一下对手`
- 市场：`市场调研`、`行业分析`、`用户需求`
- 技术：`技术调研`、`方案调研`、`可行性分析`
- 反馈：`舆情分析`、`用户反馈`、`评论分析`
- 决策：`开会讨论`、`讨论一下`、`帮我判断`
- 审查：`审查`、`review`、`验收`、`找问题`
- 策略：`制定策略`、`路线图`、`行动方案`

平台无关的 intent 路由见：

```text
protocol/intent-routing.md
```

跨项目任务配方见：

```text
recipes/
```

其中 `research-to-video` 覆盖选题研究、资料调研到视频 brief、分镜、媒体执行记录和质量门禁。

Codex 平台只负责把这些 intent/recipe 映射到当前可用能力，见：

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

### 2. 选择 intent、mode 和 recipe

按 `protocol/intent-routing.md` 识别通用任务意图，并在 `recipes/` 中选择任务配方。

think-tank core 不内置固定触发词。自然语言触发、项目偏好和 provider 选择应由 routing policy 配置：

```text
routing/policy-schema.md
platforms/<platform>/provider-policy.example.yaml
```

如果平台或项目没有配置 policy，按协议默认路径保守降级，不得伪造某个触发词已经绑定外部 skill。

常用 intent：

- `general_research`
- `competitive_intelligence`
- `market_research`
- `technical_research`
- `user_feedback_analysis`
- `media_research`
- `research_to_video`
- `decision_council`
- `review_acceptance`
- `strategy_planning`
- `monitoring_plan`
- `synthesis`

按 `protocol/mode-selection.md` 选择：

- `research`：研究、信息收集、证据整理
- `council`：多角色讨论、审议、决策
- `review`：审查、验收、问题发现
- `strategy`：路线、产品、架构和优先级

如果无法判断，默认使用 `council`，并说明原因。

recipe 可以建议 profiles、capabilities 和 optional peer skills，但不能把外部 peer skills 变成 core 依赖。

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
- `media-production`
- `social-listening`
- `knowledge-persistence`
- `browser-automation`

capability 不是具体工具。平台 adapter 负责把 capability 映射成当前可用的 skills、工具或执行步骤。

### 5. 路由到 optional peer skills

当 recipe 或 capability 需要外部能力时，按 `routing/` 形成中间连接决策：

```text
recipe.required_capabilities
  + platform available provider registry
  + task constraints
  -> skill_route
  -> dispatch_decision
  -> result_recovery
```

必须遵守：

```text
routing/skill-router.md
routing/dispatch-policy.md
routing/result-recovery.md
```

routing 层只选择和连接当前平台声明的能力提供者，不改变 think-tank core。provider 缺失、未授权或失败时，必须降级到 core protocol、用户材料或本地材料，并在边界中说明。

如果当前平台是 Claude Code，并且任务需要调用外部 skill/tool，必须遵守：

```text
platforms/claude-code/dispatch-contract.md
```

也就是说，在调用外部 skill/tool 前必须形成 `dispatch_decision`，调用后必须形成 `dispatch_log`，并将结果回收到 `sources[]`、`evidence[]` 或对应输出结构。

### 6. 平台执行

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

### 7. 汇总输出

最终输出必须回到 think-tank 结构：

```yaml
runtime_provenance:
  think_tank_runtime_used: true | false
  provider_policy_checked: true | false
  dispatch_decision_emitted: true | false
  provider_invoked: true | false
  result_recovered: true | false
  true_multi_agent_runtime: true | false
  execution_method: full_runtime | adapter_runtime | direct_tool_call | single_agent_multi_profile | manual_synthesis | protocol_only
  data_collection: provider_managed | direct_assistant_tool | user_provided | local_files | none
  evidence_state: planned | mock | installed | discovered | selected | dispatched | invoked | recovered | verified_partial | verified | blocked | failed | tracking
  result_recovery: automatic | manual | none
  boundaries: []
```

```text
结论
依据
角色观点
分歧与风险
行动建议
边界
```

项目分析、竞品策略、市场进入或需要沉淀到项目的任务，还必须使用：

```text
protocol/evidence-sources.md
protocol/artifact-quality-gates.md
protocol/artifact-write-policy.md
protocol/strategy-to-backlog.md
protocol/post-run-curation.md
recipes/project-competitive-strategy.md
```

并按任务需要输出：

```yaml
evidence_sources:
  local_code: []
  local_docs: []
  web_sources: []
  user_provided: []
  inference: []
  unavailable_data: []
strategy_to_backlog:
  backlog_candidates: []
artifact_plan:
  write_requested_by_user: true | false
  destination: ""
  overwrite_existing: false
  git_impact: none
  private_data_check: true
post_run_curation:
  required: true | false
  should_persist: true | false
  source_candidates: []
  trend_candidates: []
  action_candidates: []
  generated_artifacts: []
  artifact_plan: {}
  persistence_decision:
    wrote_files: true | false
    reason: ""
  boundaries: []
```

`post_run_curation` 是 think-tank core 的通用收尾能力。研究、趋势、竞品、市场、用户反馈、策略、审查、监控、宣传或内容规划任务结束时，都应判断是否需要输出该块。`.think-tank/`、Obsidian、项目文档或其他知识系统只是可能的落点，不是这项能力的来源。

轻量任务可以合并栏目，但不能丢失结论、风险和行动建议。

如果只是按 think-tank 结构输出，但没有真实走 runtime 或 provider dispatch，
必须明确写出 `think_tank_runtime_used: false` 或相应降级状态。直接使用助手工具收集资料
时必须写 `data_collection: direct_assistant_tool`，不能说成 provider-managed
source-acquisition。单 agent 分角色分析必须写 `true_multi_agent_runtime: false`。

### 8. 质量检查

输出前检查：

- 是否明确 mode
- 是否说明角色或视角
- 是否区分事实、推断和建议
- 是否列出分歧或风险
- 是否给出可执行下一步
- 是否说明未验证或受限部分
- 是否没有把 mock/tracking/planned 说成 verified
- 是否没有把 single-agent fallback 说成 specialist subagent runtime
- 是否包含 `runtime_provenance`
- 是否没有把 direct assistant tool use 写成 provider invocation
- 是否没有把 role labels 写成真实独立 subagents
- 是否在 research、trend、competitive、strategy、review、monitoring、promotion 或 content planning 任务中给出 `post_run_curation`，并说明是否实际写入
- 是否在生成媒体、报告、样例、演示或 run record 时执行 `protocol/artifact-quality-gates.md`，并保留 `generated_artifacts`、验证命令和 known gaps

## 外部 skills 共存规则

think-tank 可以编排外部 skills，但不拥有它们。

外部 skill 名称只能来自当前平台 adapter 的运行时发现结果、项目本地 registry 或用户显式指定，不能由主协议或通用 router 写死。

示例关系应该这样表达：

- 视频研究：`media-processing` -> 当前平台可用的媒体处理 provider
- 媒体成品：`media-production` -> 当前平台可用的素材、口播、字幕、渲染和 probe provider
- 社媒舆情：`social-listening` -> 当前平台可用且已授权的社媒样本 provider
- 知识沉淀：`knowledge-persistence` -> 当前平台可用且已授权的知识 artifact provider
- 浏览器任务：`browser-automation` -> 当前平台可用的只读浏览器或页面读取 provider

如果外部 skill 不可用，按 capability 的降级策略处理，并在边界中说明。

recipe 中出现的 `optional_peer_skills` 只表示候选实现：

```yaml
optional_peer_skills_are_dependencies: false
missing_peer_skill_behavior: degrade_to_core_protocol
execution_claim: only_verified_per_run
```

## 旧资产关系

- 旧 research agent 是 research mode、capabilities、profiles 和 Claude Code 映射的来源材料。
- 旧 agent-council 是 council mode 和 Claude Code runtime contract 的来源材料。
- 私有领域知识不进入主仓 core；需要时由具体项目自行提供 domain pack 或本地资料。

## 能力状态

任何平台能力都必须标注：

- `verified`：真实执行并验证
- `mock`：只在模拟路径验证
- `tracking`：只记录状态，不代表执行完成
- `planned`：设计目标，尚未实现

## 入口文档

- 架构总览：`docs/architecture.md`
- 核心协议：`protocol/think-tank-protocol.md`
- intent 路由：`protocol/intent-routing.md`
- mode 选择：`protocol/mode-selection.md`
- 通用 recipes：`recipes/`
- 技能路由中间层：`routing/`
- routing policy schema：`routing/policy-schema.md`
- profiles：`profiles/`
- profile prompt pack：`profiles/prompt-pack.md`
- capabilities：`capabilities/`
- 平台适配：`platforms/`
