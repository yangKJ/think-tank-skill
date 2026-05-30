# Codex Long-Running Adapter Runtime Validation

本文记录 Codex 平台上一条真实的长生命周期 adapter runtime 样例。

## 测试任务

```text
AI快报：把今天的AI资讯做成视频
```

## 执行声明

```yaml
platform: codex
runtime: codex-natural-language-orchestrator
intent: research_to_video
mode: research
provider: ai-research-to-video-production
status: verified_partial
dispatch_decision:
  route_selected: local-ai-tech-news-video-production
  provider_selected: ai-research-to-video-production
  provider_preflight: ready
runtime_provenance:
  true_multi_agent_runtime: false
  execution_method: adapter_runtime
  authority_level: full_runtime
  result_recovery: automatic
```

## Lifecycle

```yaml
steps:
  - init_video_run
  - write_handoff_artifacts
  - prepare_voiceover_manifest
  - synthesize_voiceover
  - create_subtitle_timeline
  - render_sfx
  - synthesize_bgm
  - create_cover_package:bilibili
  - create_cover_package:youtube
  - render_research_video_layout
  - create_delivery_report
```

## 回收结果

```yaml
run_record:
  artifact_written: true
  artifact_path: .think-tank/runs/nlrt-cf00e9c29ca1.json
generated_artifacts:
  run_dir: .think-tank/artifacts/media/auto-video-runs/video-run-20260521-ai快报-把今天的ai资讯做成视频
  render_output: .think-tank/artifacts/media/auto-video-runs/video-run-20260521-ai快报-把今天的ai资讯做成视频/renders/final-news.mp4
  delivery_report: .think-tank/artifacts/media/auto-video-runs/video-run-20260521-ai快报-把今天的ai资讯做成视频/video_delivery_report.json
delivery_status: publish_candidate
```

## 关键观察

1. `ai-research-to-video-production` 在当前机器上完成了真实 provider invocation，而不是只有 policy selection。
2. source-acquisition 对 `https://example.com` 的本地读取因权限边界失败，但没有伪造来源结果。
3. 下游 video adapter 仍然完成了 run 初始化、脚本、字幕、SFX、BGM、封面包、渲染和交付报告。
4. 这证明 Codex 已有一条真实的 long-running adapter lifecycle recovery 路径。

## 结果判断

该样例可以把 `ai-research-to-video-production` 提升为公开 `verified_partial` provider 证据，并证明：

- provider preflight
- dispatch decision
- provider invocation
- artifact recovery
- multi-step lifecycle continuation

已经在同一条真实运行链路里发生。

但它**不能**证明：

- true multi-agent runtime
- long-running subagent lifecycle
- 登录态网页或复杂外部 source-acquisition

## 边界

- 本次运行的 `true_multi_agent_runtime` 明确为 `false`。
- 语音合成阶段依赖 fallback，而不是证明外部语音 provider 稳定可用。
- 该样例属于 long-running adapter runtime，不应偷换成 subagent lifecycle verified。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```
