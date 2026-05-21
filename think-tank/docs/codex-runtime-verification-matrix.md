# Codex Runtime Verification Matrix

本文汇总 Codex 平台的真实 runtime 验证矩阵。

## Current Status

```yaml
platform: codex
core_skill_ready: true
yaml_policy_routing: verified
provider_registry: verified
true_multi_agent_council: verified_partial
provider_invocation_matrix: established
claude_code_runtime: deferred
```

## Multi-Agent Runtime

| runtime | status | evidence | boundary |
|---------|--------|----------|----------|
| single_agent_multi_profile | verified | `examples/codex-council-validation.md` | 单 agent 模拟多 profile |
| codex_parallel_subagents | verified_partial | `examples/codex-true-council-runtime.md` | 只读 repo 分析和 role_result 回收 |
| claude_code_team_runtime | deferred | `platforms/claude-code/` | 当前阶段不验证 |

## Provider Invocation

| provider | capability | status | evidence | boundary |
|----------|------------|--------|----------|----------|
| local_static_reader | source-acquisition | verified | `examples/codex-provider-invocation-matrix.json` | 本地静态文件 |
| agent-reach | source-acquisition | available_not_verified | `provider-policy.example.yaml` | 统一入口分派，不直接执行抓取 |
| public_http_static_reader | source-acquisition | verified_partial | `examples/codex-provider-invocation-matrix.json` | HTTP 成功，HTTPS 本地证书失败 |
| playwright-cli | browser-automation | verified_partial | `examples/codex-provider-invocation-matrix.json` + `examples/codex-browser-external-readonly.md` | 外部静态页面只读 DOM 回收；不含登录态和交互 |
| web-access | source-acquisition | available_not_verified | `provider-policy.example.yaml` | policy selection only |
| taskflow | knowledge-persistence | available_not_verified | `provider-policy.example.yaml` | policy selection only |
| xiaohongshu | social-listening | available_not_verified | `provider-registry.md` | 未真实调用 |
| yt-dlp | media-processing | available_not_verified | `provider-registry.md` | 未真实调用 |
| obsidian | knowledge-persistence | available_not_verified | `provider-registry.md` | 未真实写入 |

## YAML Policy Loop

| trigger | route | mode | provider behavior |
|---------|-------|------|-------------------|
| 研究一下 | general-research-default | research | selects agent-reach, does not invoke |
| 竞品分析 | competitive-intelligence | research | selects agent-reach, does not invoke |
| 开会讨论 | council-discussion | council | no provider selected because no capability is required |
| 审查 | review-acceptance | review | selects agent-reach, does not invoke |
| 制定策略 | strategy-planning | strategy | no provider selected because no capability is required |
| 持续关注 | monitoring-plan | strategy | selects taskflow, does not invoke |

## Fixed During Verification

- `council-discussion` 原本在没有 capability 的情况下会默认选择 `web-access`。
- 已修复为：无 capability 且无显式 provider 偏好时，不选择 provider。
- `source-acquisition` 的默认路由已改为优先 `agent-reach`，并保持 policy selection 与 runtime invocation 的边界。
- 已新增 `strategy-planning` route 支持 `制定策略`、`策略规划`、`路线规划` 等触发词。

## Acceptance Boundary

```yaml
can_claim:
  - Codex true multi-agent council verified_partial
  - local source-acquisition verified
  - public HTTP static source-acquisition verified_partial
  - playwright external readonly DOM capture verified_partial
  - YAML trigger routing verified
cannot_claim:
  - all peer skills are executable
  - all external providers are automatically invoked
  - external browser interaction or login automation is verified
  - Claude Code runtime is verified
```
