# Codex Smoke Research Result

本文件记录一次在 Codex 平台执行的 think-tank smoke test。

## 测试任务

```text
研究一个跨平台 Skill 仓库应该如何组织目录结构，要求给出通用建议、风险和下一步行动。
```

## 执行声明

```yaml
platform: codex
execution_method: single_agent_profile_simulation
mode: research
profiles:
  - source-collector
  - trend-analyst
  - skeptic
  - report-architect
capabilities:
  - source-acquisition
  - knowledge-persistence
verified:
  - protocol_readability
  - mode_selection
  - profile_selection
  - capability_selection
  - local_repository_collection
  - structured_output
not_verified:
  - claude_code_agent_team
  - external_skill_invocation
  - true_parallel_multi_agent_execution
```

## 结论

一个跨平台 Skill 仓库应该采用“协议核心 + 平台适配 + 能力槽 + 角色模板 + 可选领域包”的分层结构。

think-tank 当前仓库结构已经满足第一版跨平台主 Skill 的基本要求：协议层不绑定平台，平台适配不改写协议，外部工具型 skills 通过 capabilities 共存，旧 subagents 通过 profiles 被抽象，私有领域知识不进入 core。

## 依据

本次 smoke test 读取了当前仓库结构和关键文件：

- `think-tank/SKILL.md`：已定义执行入口、mode/profile/capability 选择和输出结构。
- `think-tank/docs/architecture.md`：已定义 protocol、modes、profiles、capabilities、platforms、domain-packs 的职责边界。
- `think-tank/protocol/`：已包含核心协议、输入输出、角色选择、mode 选择、质量门禁和版本规则。
- `think-tank/profiles/`：已包含跨平台角色模板。
- `think-tank/capabilities/`：已包含外部能力槽。
- `think-tank/platforms/codex/`：已包含 Codex adapter、capability mapping 和 smoke test。

## 角色观点

### source-collector

当前仓库已经具备可验证的本地结构证据：

```text
protocol/
modes/
profiles/
capabilities/
platforms/
domain-packs/
schemas/
examples/
docs/
```

这些目录能够分别承载协议、场景、角色、工具能力、平台差异、领域扩展、机器契约、示例和说明。

### trend-analyst

跨平台 Skill 的核心趋势是避免把能力写死到某个 runtime。think-tank 当前结构把旧 research agent 的 tools 和 subagents 拆为 capabilities 和 profiles，这比复制旧 `.claude/skills` 更适合长期复用。

最重要的架构方向是：

- core 只定义协议和行为
- adapter 处理平台实现
- capability 连接外部 tools
- profile 抽象角色
- domain pack 承接领域经验

### skeptic

当前结构仍有几个风险：

- 文档较多，后续需要避免重复和漂移。
- Codex smoke test 只能证明单 agent 多 profile 模拟，不证明真实多 agent 协作。
- Claude Code Agent Team 仍然需要独立验证。
- 外部 skills 只是候选映射，并未在本仓执行集成测试。
- domain pack 仍是扩展点，当前主仓不内置私有领域包。

### report-architect

当前仓库适合作为 `0.1.0` 基础版本，但应该明确定位为协议和结构版本，而不是 runtime 完成版本。

第一版对外说明应强调：

- 已完成主架构和协议边界。
- Codex 路径可进行单 agent 协议执行。
- Claude Code 路径仍是 planned，需后续验证。
- 外部 skills 通过 capability mapping 共存，不被内置。

## 分歧与风险

- 分歧：是否现在就加入运行时脚本。结论是暂不加入，先稳定协议和适配契约。
- 风险：文档架构如果继续增长，可能出现多处定义同一概念。
- 风险：如果后续没有真实平台验证，`capabilities` 和 `profiles` 会停留在设计层。
- 风险：外部用户可能误以为 think-tank 自带 `yt-dlp`、`obsidian`、`xiaohongshu` 等工具，需要在 README 中持续强调“不复制工具，只编排能力”。

## 行动建议

1. 保持当前目录分层，不再把旧 research agent 原样迁入 core。
2. 将当前版本标记为 `0.1.0 foundation`。
3. 下一步在 Claude Code 平台验证 agent mapping 和 skill mapping。
4. 为 Codex 路径补一个更正式的 `v0.1-readiness.md`。
5. 后续新增 domain pack 前，先确认它是否适合进入通用主仓；私有领域知识应留在具体项目。

## 边界

- 本次测试没有联网。
- 本次测试没有调用外部 skills。
- 本次测试没有启动 Claude Code Agent Team。
- 本次测试没有真实并行 subagent。
- 本次测试验证的是 Codex 单 agent 多 profile 协议执行路径。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```
