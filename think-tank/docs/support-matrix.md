# Support Matrix

本文定义公开 `think-tank` 当前真正支持到什么程度。

## Release Summary

```yaml
release_posture: public_beta
default_platform: codex
default_runtime: single_agent_multi_profile
multi_agent_runtime: verified_partial_for_readonly_council_only
external_provider_runtime: per_provider_validation_required
current_default_release: full_repo_public_beta
```

Packaging:

- leader-runtime packaging: included in current repository release
- skill-only packaging: optional future split

## Core Workflow

| area | status | notes |
|------|--------|-------|
| protocol structure | verified | 公开协议和目录结构可检查 |
| research mode | verified | Codex 主路径已验收 |
| council mode | verified | 默认是单 agent 多 profile；只读 subagent council 是 `verified_partial` |
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
| browser-automation | verified_optional_localhost | localhost fixture | 外部网页仍未声明通用可用 |
| knowledge-persistence | verified_for_markdown_artifact | repository markdown artifact | 不默认写私有知识库 |
| media-processing | degraded_verified | fallback to user-provided material | 不默认下载或转录媒体 |
| social-listening | degraded_verified | fallback to user-provided samples | 不默认抓取社媒 |

## Provider Support

| provider | status | notes |
|----------|--------|-------|
| local_static_reader | verified | 仓库内本地文件路径 |
| public_http_static_reader | verified_partial | 公网静态页面只读样例 |
| playwright-cli | verified_partial | localhost read-only DOM snapshot |
| agent-reach | available_not_verified | policy 可选中，但不默认声称已调用 |
| web-access | available_not_verified | 需要单独 invocation 证据 |
| taskflow | available_not_verified | policy 可选中，不默认写外部状态 |
| obsidian | planned | 不默认写入 |
| yt-dlp | planned | 尚未做公开稳定承诺 |
| xiaohongshu | planned | 尚未做公开稳定承诺 |

## Not Claimed

当前明确不对外声称：

- full cross-platform multi-agent runtime
- arbitrary provider invocation
- browser external DOM recovery as generally available
- private knowledge-base write by default
- social media scraping by default
- every installed peer skill being executable
