# Provider Ecosystem Examples

本文展示 `think-tank` 如何把真实同级 skills 作为可选 provider 生态接入。它不是内置能力清单，也不是默认安装承诺。

## Core Boundary

```yaml
think_tank_core:
  role: task understanding + role organization + capability routing + evidence synthesis + boundary declaration
  bundles_peer_skills: false
peer_skills:
  role: concrete capability providers
  status: optional_ecosystem_examples
  must_report:
    - route_selected
    - dispatch_decision
    - invoked_providers
    - not_invoked_providers
    - recovery
    - verification_status
```

## Representative Providers

| capability slot | representative peer skill | why it is useful | current public status | requires | not claimed |
|---|---|---|---|---|---|
| source-acquisition | `web-access` / `agent-reach` | external source discovery and page reading | available_not_verified | network, per-run permission | default verified provider invocation |
| browser-automation | `playwright-cli` / Browser | readonly page snapshots and browser fixtures | verified_partial | browser runtime, task permission | login flows or dynamic app automation |
| social-listening | `xiaohongshu` | social sample collection when user has access | planned | MCP service, login, platform permission | default social scraping |
| media-processing | `yt-dlp` / `openai-whisper` | media download, audio extraction, transcript workflows | planned | network, media rights, task permission | default media download or transcription |
| knowledge-persistence | `obsidian` | optional local knowledge artifact persistence | planned | vault path, explicit write confirmation | default private knowledge-base write |
| media-production | `research-to-video-production` | structured brief to production package workflow | verified_partial | task-specific media boundary | fully automated publishing |

## Evidence Rule

Provider examples are credible only when the output distinguishes:

```text
selected != dispatched != invoked != recovered != verified
```

If a provider was only discovered or selected by policy, list it under `not_invoked_providers` or `available_not_verified`.

## Visual Map

See:

```text
think-tank/assets/diagrams/provider-ecosystem.svg
```
