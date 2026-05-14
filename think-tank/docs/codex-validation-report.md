# Codex Validation Report

本文记录 think-tank 在 Codex 平台的内部验证结果。

## 验证范围

本轮验证范围：

```yaml
platform: codex
execution_method: single_agent_profile_simulation
external_skills_installed_or_invoked: false
claude_code_agent_team_invoked: false
network_required: false
```

本轮目标是验证 think-tank core 在 Codex 平台是否能执行，而不是验证外部 skills 或 Claude Code runtime。

## 验证结果

```yaml
codex:
  research_mode: verified
  council_mode: verified
  review_mode: verified
  strategy_mode: verified
  minimal_install_behavior: verified
  codex_operational_usage: verified
  local_source_markdown_artifact: verified
  external_source_readonly: verified
  protocol_check: verified
  codex_validation_check: verified
  schema_sample_check: verified
  browser_automation_localhost: verified_optional
  browser_automation_external_web: blocked
  external_skill_invocation: planned
  true_multi_agent_execution: planned
```

## 验证产物

| mode | 文件 | 状态 |
|------|------|------|
| research | `examples/codex-smoke-research.md` | verified |
| council | `examples/codex-council-validation.md` | verified |
| review | `examples/codex-review-validation.md` | verified |
| strategy | `examples/codex-strategy-validation.md` | verified |
| minimal install | `examples/codex-minimal-install-validation.md` | verified |
| operational usage | `examples/codex-operational-validation.md` | verified |
| local source + artifact | `examples/codex-local-source-validation.md` | verified |
| external source readonly | `examples/codex-external-source-validation.md` | verified |
| browser external readonly | `examples/codex-browser-external-blocked.md` | blocked |

## Research Mode

测试任务：

```text
研究一个跨平台 Skill 仓库应该如何组织目录结构，要求给出通用建议、风险和下一步行动。
```

验证结果：

- mode 选择正确
- profiles 选择正确
- capabilities 选择正确
- 本地仓库证据收集可行
- 输出结构满足协议
- 边界声明清楚

状态：

```yaml
research_mode:
  status: verified
  limitation: 本次只验证本地仓库研究，不验证外部 source acquisition skill
```

## Council Mode

测试任务：

```text
开会讨论：think-tank 当前把 capabilities 和 profiles 拆成两层是否合理？
```

验证结果：

- 能模拟 facilitator、trend analyst、skeptic、product strategist、report architect 多视角讨论
- 能记录共识、分歧、风险和行动建议
- 能明确不声称真实多 agent debate

状态：

```yaml
council_mode:
  status: verified
  limitation: 单 agent 多 profile 模拟，不验证 Claude Code SendMessage 或 L1/L2/L3 runtime
```

## Review Mode

测试任务：

```text
审查 v0.1.0 foundation 文档是否存在概念冲突、遗漏或过度设计。
```

验证结果：

- 能按 review mode 做结构化审查
- 能按严重程度列风险
- 能区分已验证能力和未验证能力
- 能输出下一步行动

状态：

```yaml
review_mode:
  status: verified
  limitation: 当前检查以文档和本地结构为主，不做语义级自动化验证
```

## Strategy Mode

测试任务：

```text
为 think-tank v0.1 之后的建设制定下一阶段路线：先继续验证 Codex 外部能力，还是切换到 Claude Code 平台验证？
```

验证结果：

- 能按 strategy mode 比较路线选择
- 能拆分阶段、退出标准和风险
- 能避免把 Claude Code 旧实现重新放回主协议中心
- 能输出下一步行动

状态：

```yaml
strategy_mode:
  status: verified
  limitation: 单 agent 多 profile 模拟，不验证真实多 agent 战略会话
```

## 当前结论

think-tank 在 Codex 平台的内部协议执行路径已经可以继续使用。

可以信任的能力：

- 根据任务选择 mode
- 根据 mode 选择 profiles
- 根据任务选择 capabilities
- 在 Codex 中做单 agent 多 profile 模拟
- 使用本地仓库作为证据源
- 将本地研究结论沉淀为仓库内 Markdown artifact
- 对公开静态网页做 Codex 外部只读 source acquisition
- 输出结构化结论、风险和行动建议
- 运行 `checks/protocol_check.py`
- 运行 `checks/codex_validation_check.py`

不能声称的能力：

- 已真实调动外部 skills
- 已真实多 agent 并行执行
- 已验证 Claude Code Agent Team
- 已验证 `.claude/skills` 和 `.claude/agents` 映射
- 已验证 Browser 外部网页 DOM 回收

## Codex 验收命令

```bash
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/claude_code_validation_check.py
python3 checks/claude_dispatch_sample_check.py
python3 checks/claude_runtime_sample_check.py
python3 checks/schema_sample_check.py
```

六个命令都通过，才可以说当前仓库验证产物完整。Codex foundation 仍以 `protocol_check`、`codex_validation_check` 和 `schema_sample_check` 为核心。

## 是否可以安装其他技能

当前判断：**可以继续做低风险 optional capability 的最小集成测试，但不应把外部技能列为 core dependency。**

原因：

1. 四个核心 mode 已完成 Codex 内部验证。
2. capability 降级测试已经完成。
3. Browser 作为第一个 optional capability 已完成 localhost fixture 验证。
4. 其他外部 skill 仍会引入依赖、权限、登录、网络、路径和输出格式变量。

## 下一阶段

进入更多外部 skill 集成测试前，先保持以下顺序：

```yaml
next_phase: claude_code_preflight_or_second_optional_capability
tests:
  - prepare_claude_code_preflight_checklist
  - or_verify_one_more_low_risk_optional_capability
```

降级测试结果记录于：

```text
think-tank/docs/capability-degradation-report.md
```

建议第一个外部能力测试：

```yaml
first_external_capability_candidate: browser-automation
reason: Codex 环境最接近已有浏览器和 Playwright 能力，风险低于 xiaohongshu/obsidian/yt-dlp
status: completed_for_localhost_fixture
```

## 后续验收门槛

只有满足以下条件后，才建议进入外部 skill 安装或接入：

- Codex research/council/review 已验证
- capability 降级测试通过
- validation report 明确边界
- 只选择一个 capability 做最小集成
- 失败时能回退并标注边界
