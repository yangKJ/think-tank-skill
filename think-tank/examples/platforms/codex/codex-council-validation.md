# Codex Council Validation

本文件记录 Codex 平台对 council mode 的验证。

## 测试任务

```text
开会讨论：think-tank 当前把 capabilities 和 profiles 拆成两层是否合理？
```

## 执行声明

```yaml
platform: codex
execution_method: single_agent_profile_simulation
mode: council
profiles:
  - facilitator
  - trend-analyst
  - skeptic
  - product-strategist
  - report-architect
capabilities:
  - source-acquisition
  - knowledge-persistence
verified:
  - council_mode_selection
  - profile_based_deliberation
  - disagreement_recording
  - structured_recommendation
not_verified:
  - true_multi_agent_debate
  - claude_code_send_message
  - l1_l2_l3_runtime_state_machine
```

## 结论

`capabilities` 和 `profiles` 拆成两层是合理的，而且对跨平台 think-tank 是必要的。

核心原因是：profile 解决“谁以什么视角思考”，capability 解决“需要什么外部能力”。如果混在一起，旧 research agent 的工具、subagent、领域经验会再次绑定，think-tank 就会退化成某个平台或某个领域的私有系统。

## 角色观点

### facilitator

议题可以拆为两个问题：

1. `profiles` 是否应该独立于平台 subagents？
2. `capabilities` 是否应该独立于工具型 skills？

当前文档已经把这两者分开：

- `profiles/` 定义跨平台角色模板。
- `capabilities/` 定义外部能力槽。
- `platforms/claude-code/` 再负责把旧 `.claude/agents` 和 `.claude/skills` 映射进去。

### trend-analyst

从长期演进看，拆分是正确方向。市面上的 skills 会变化，平台 runtime 也会变化，但角色视角和能力需求更稳定。

例如：

- `social-listener` 可以在 Claude Code 映射到 `xiaohongshu`，在其他平台映射到不同社媒工具。
- `media-processing` 可以由 `yt-dlp`、Whisper、本地 CLI 或未来平台内置能力实现。

这种设计避免 think-tank 被某个工具生态锁死。

### skeptic

拆分也带来风险：

- 概念层增加，用户可能不理解 profile 和 capability 的区别。
- 文档容易重复，比如 source collector 和 source acquisition 都提到来源。
- 平台 adapter 如果不够清楚，可能不知道先选 profile 还是先选 capability。
- 外部 skill 的真实调用尚未验证，capability 目前仍偏设计层。

这些风险需要通过更好的架构说明、示例和 validation report 降低。

### product-strategist

从产品化角度，拆分是必要的，但需要给用户一个简单心智：

```text
mode = 要做什么场景
profile = 谁来思考
capability = 需要什么能力
platform = 怎么执行
```

后续 README 和使用说明应坚持这个表达，避免用户被内部层次淹没。

### report-architect

最终建议是保留拆分，但加强示例。

当前结构应继续沿用：

```text
profiles/       # 角色
capabilities/   # 能力
platforms/      # 执行映射
domain-packs/   # 领域知识
```

## 分歧与风险

- 共识：拆分合理。
- 分歧：是否需要进一步减少概念数量。当前结论是不减少，但通过文档和示例降低理解成本。
- 风险：如果后续 adapter 没有真实执行，capabilities 可能停留在抽象层。
- 风险：外部用户可能把 capability 误解成内置工具。

## 行动建议

1. 保留 `capabilities/` 和 `profiles/` 两层。
2. 在 README 和 usage 中持续使用 `mode/profile/capability/platform` 四段式解释。
3. 在外部 skill 测试前，先完成 Codex review mode 验证。
4. 后续外部 skill 测试从单一 capability 开始，不要一次接入全部旧 skills。

## 边界

本次 council mode 在 Codex 中以单 agent 多 profile 模拟执行。它验证了结构化审议和分歧记录，不验证真实多 agent 辩论、Claude Code `SendMessage` 或 L1/L2/L3 状态机。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

