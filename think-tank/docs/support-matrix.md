# Support Matrix

本文定义公开 `think-tank` 当前真正支持到什么程度。

## Release Summary

```yaml
release_posture: stable_release
default_platform: codex
default_runtime: codex_first_runtime_with_explicit_boundaries
multi_agent_runtime: verified_partial_with_scoped_write_lifecycle
external_provider_runtime: per_provider_validation_required
current_default_release: skill_core_only_bundle
```

Packaging:

- leader-runtime packaging: moved to standalone sibling project
- skill-only packaging: current default release

## Core Workflow

| area | status | notes |
|------|--------|-------|
| protocol structure | verified | 公开协议和目录结构可检查 |
| research mode | verified | Codex 主路径已验收 |
| council mode | verified | 默认是 Codex-first runtime；readonly council 与 scoped write lifecycle 都有 `verified_partial` 证据 |
| review mode | verified | 可用于结构化审查 |
| strategy mode | verified | 可用于路线和决策分析 |
| runtime provenance | verified | 输出必须披露 runtime 和证据边界 |
| capability degradation | verified | capability 缺失时可降级并声明边界 |

## Platform Support

| platform | status | notes |
|----------|--------|-------|
| Codex | verified_foundation | 当前公开主平台 |
| Claude Code | deferred | 协议和 adapter 文档存在，不声明完整 runtime verified |
| other platforms | planned | 需要独立 adapter 和验收 |

## Capability Support

| capability | status | default path | notes |
|------------|--------|--------------|-------|
| source-acquisition | verified | local files + user-provided material | 公开静态 HTTP 来源是 `verified_partial` |
| browser-automation | verified_optional_readonly | external readonly + localhost fixture | 不声明登录态、点击交互或复杂动态网页可用 |
| knowledge-persistence | verified_for_markdown_artifact | repository markdown artifact | 不默认写私有知识库 |
| media-processing | degraded_verified | fallback to user-provided material | 不默认下载或转录媒体 |
| social-listening | degraded_verified | fallback to user-provided samples | 不默认抓取社媒 |

## Provider Support

| provider | status | default included? | login? | network? | permission? | safe fallback | do not claim |
|----------|--------|-------------------|--------|----------|-------------|---------------|--------------|
| local_static_reader | verified | yes | no | no | no | user-provided material | external provider runtime |
| public_http_static_reader | verified_partial | yes | no | yes | task-dependent | user-provided excerpt | broad web automation |
| playwright-cli | verified_partial | optional | no for readonly fixtures | yes for external pages | yes before automation | static snapshots or user-provided excerpt | login, click flows, or dynamic app automation |
| research-to-video-production | verified_partial | optional | no by default | task-dependent | yes before media production | markdown brief | fully automated publishing |
| agent-reach | available_not_verified | no | provider-dependent | provider-dependent | yes | core protocol synthesis | invoked provider |
| web-access | available_not_verified | no | provider-dependent | yes | yes | user-provided excerpt | verified source acquisition |
| taskflow | available_not_verified | no | provider-dependent | provider-dependent | yes before writes | markdown artifact | external state write |
| obsidian | planned | no | local vault access | no by default | yes before private write | markdown artifact | default private knowledge write |
| yt-dlp | planned | no | no | yes | yes before download | user-provided transcript | default media download |
| xiaohongshu | planned | no | yes | yes | yes | user-provided samples | default social scraping |

## Not Claimed

当前明确不对外声称：

- full cross-platform multi-agent runtime
- arbitrary provider invocation
- browser interaction, login, or dynamic app automation as generally available
- private knowledge-base write by default
- social media scraping by default
- every installed peer skill being executable

## Validation Tiers

公开发布只依赖 release gate。更深的 core validation 和 local provider validation 见：

```text
think-tank/docs/validation-tiers.md
```
