# Claude Code Capability Discovery

本文件记录 Claude Code 平台对 think-tank capability 到旧 `.claude/skills` 映射的发现验证。

## 测试任务

```text
使用 think-tank research mode，验证 Claude Code adapter 是否能发现当前可用的 browser/source acquisition 类 skills，并在不执行高风险操作的情况下列出 capability 到 skill 的映射、可用性、降级路径和未验证边界。
```

## 执行声明

```yaml
platform: claude-code
mode: research
execution_method: skill_discovery_only
selected_profiles:
  - source-collector
selected_capabilities:
  - browser-automation
  - source-acquisition
external_skills_invoked: false
high_risk_operations: false
status: skills_detected_mapping_mock
verified:
  - think_tank_skill_loaded
  - installed_skill_directories_listed
  - browser_source_related_skills_detected
  - capability_to_skill_mapping_reported
  - no_external_skill_execution_overclaim
not_verified:
  - capability_auto_mapping_logic
  - external_skill_invocation
  - result_recovery_contract
  - fallback_runtime_behavior
  - multi_profile_parallel_execution
```

## Available Skills Detected

| skill | detected path | mapped capability | status |
|-------|---------------|-------------------|--------|
| `web-access` | `research/.claude/skills/` | `browser-automation` / `source-acquisition` | installed |
| `playwright-cli` | `research/.claude/skills/` | `browser-automation` | installed |
| `google-ai-mode-skill` | `research/.claude/skills/` | `source-acquisition` | installed |
| `mcp-cli` | `research/.claude/skills/` | `source-acquisition` | installed |
| `juejin-search` | `research/.claude/skills/` | `source-acquisition` | installed |
| `36kr-hotlist` | `research/.claude/skills/` | `source-acquisition` | installed |

## Capability Status

```yaml
browser_automation:
  status: mock
  reason: skills 已安装，但未通过 think-tank adapter 自动调度，也未执行端到端调用

source_acquisition:
  status: mock
  reason: skills 已安装，但未通过 think-tank adapter 自动调度，也未执行端到端调用
```

## 结论

Claude Code 能发现 research 项目中已安装的 browser/source acquisition 类 skills，并能形成 capability 到 skill 的映射表。

但当前验证只证明“发现和映射可被人工列出”，不证明 think-tank adapter 已经具备自动调度、fallback 或结果回收能力。

## 依据

Claude Code 输出显示：

- `Skill(think-tank)` 成功加载。
- 读取了 capabilities 和平台适配文件。
- 列出了当前 `.claude/skills` 中的相关 skills。
- 将 `web-access`、`playwright-cli`、`google-ai-mode-skill`、`mcp-cli`、`juejin-search`、`36kr-hotlist` 映射到 `browser-automation` 或 `source-acquisition`。
- 明确标注 capability 状态为 `mock`，原因是 adapter 未实现真实调度逻辑。

## 风险

- skill 已安装不等于 skill 已执行。
- capability 映射表存在不等于 adapter 自动调度存在。
- 直接在 prompt 中调用 `Skill("web-access")` 不等于经过 think-tank capability 抽象调度。
- 如果没有结果回收格式，外部 skill 输出无法稳定进入 think-tank evidence 结构。

## 行动建议

1. 将 `skill_discovery` 标记为 verified。
2. 将 `capability_auto_mapping` 保持为 mock/planned。
3. 下一步只选择一个低风险 skill 做只读端到端调用验证。
4. 优先测试 `web-access` 或 `playwright-cli` 的公开静态网页读取，不测试登录、下载、社媒抓取或私有知识库写入。
5. 验证成功后，必须检查结果是否能转换成 think-tank `sources` 或 evidence 结构。

## 边界

本次没有真实调用 `web-access`、`playwright-cli`、`google-ai-mode-skill` 或其他外部 skills。

本次没有验证 fallback、超时、权限失败、登录态页面、多 profile 并发或结果回收机制。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

