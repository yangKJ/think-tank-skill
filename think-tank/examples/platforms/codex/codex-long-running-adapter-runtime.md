# Codex Adapter Runtime Self-Test (No Source-Recovery)

本文档是一份**自检样例**，用来证明 Codex natural-language orchestrator 在没有真实 source-recovery 发生时，能诚实地报告未发生，而不是伪造 `verified_partial` 证据。

## 测试任务

```text
把一份有来源的行业研究做成视频 brief
```

本次运行**没有**通过 `--target` 提供 source target，并且当前 `.think-tank/provider-policy.yaml` 的 `media-production-handoff` 路由没有配置 `post_dispatch` 钩子，因此：

- 没有 source-acquisition 被触发（`selected_capabilities` 为空）
- 没有 post-dispatch hook 被调用
- 没有真实产物被 recover
- `evidence_state` 正确地落到 `selected`（不是 `verified_partial`）

## 执行声明

```yaml
platform: codex
runtime: codex-natural-language-orchestrator
intent: research_to_video
mode: research
provider_selected_by_policy: remotion-render
provider_invoked: false
post_dispatch_status: not_configured
source_recovered: false
evidence_state: selected
execution_method: single_agent_multi_profile_fallback
authority_level: lower_fallback_single_context
true_multi_agent_runtime: false
verified_partial: false
```

## 关键观察

1. 本次 `policy_selected_provider` 是 `remotion-render`，但 `runtime_selected_provider` 是 `null`。这正是 orchestrator 应该做的——policy 选择不等于 runtime 调用。
2. `dispatch_log.invocation.provider_invoked = false` 与 `dispatch_log.recovery.sources_recovered = false` 互相一致：source 没被恢复，所以 provider 也没被声明为 invoked。
3. `dispatch_log.dispatch_request.target = null`，因此 `should_invoke_source` 返回 `False`，`source_result` 是 `null`，这与 JSON 里的 `source_result: null` 一致。
4. `evidence_state: selected` 准确反映了"route matched 但没有 provider invocation"的真实状态，**不是** `verified_partial`。

## 这次不能证明什么

为了避免把这份自检样例偷换成"已验证的能力证据"，下面这些**不能**用本样例证明：

- `remotion-render` 真的在当前机器上跑过
- source-acquisition 真的恢复过来源
- 多步 lifecycle（init_video_run / 渲染 / 交付报告）真的发生过
- 任何 `verified_partial` 状态的 provider 能力

## 想得到真实 verified_partial 证据怎么办

需要**同时**满足：

1. 在 `.think-tank/provider-policy.yaml` 的目标 route 上声明 `capabilities: ["source-acquisition", ...]` 并提供一个可读的 target（本地文件路径、`http(s)://` URL 或 `file://` 路径）。
2. 在同一 route 上配置 `post_dispatch`（含 `enabled: true`、`auto_invoke: true`、`provider` 与 selected provider 一致、entrypoint 存在），且 preflight 真正 cleared（`can_invoke: true`，无 `requires_permission`，无 `manual_checks`）。
3. 跑一次 `python3 think-tank/platforms/codex/runtime/orchestrator.py "..." --target <readable_target>`，让 orchestrator 真实运行 source-acquisition + post-dispatch hook。
4. 验证输出里：`source_result.sources` 非空、`post_dispatch_result.status == "success"` 且 `returncode == 0`、`runtime_provenance.evidence_state == "verified_partial"`、`runtime_provenance.execution_method == "adapter_runtime"`。

如果其中任何一步缺失，orchestrator 会诚实地把 `evidence_state` 保持在 `selected` / `failed` / `pending_manual` 等正确状态。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
provider_invocation_truthful: true
```
