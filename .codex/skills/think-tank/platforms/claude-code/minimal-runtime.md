# Claude Code Minimal Runtime

本文定义 Claude Code adapter 的最小 runtime。

它不是完整多 agent runtime，也不是外部 skill 的实现。它只解决一个问题：

> 当 think-tank 已经选出 capability 时，Claude Code adapter 如何做一次可审计的 dispatch、调用和结果回收。

## Runtime Scope

```yaml
runtime: claude-code-minimal
version: 0.1.0
scope:
  - source-acquisition
  - public_static_web_read
  - single_profile
  - single_tool_invocation
out_of_scope:
  - subagent_parallel_execution
  - fallback_execution
  - login_state
  - media_download
  - private_knowledge_write
```

## Runtime Pipeline

```text
dispatch_request
  -> dispatch_decision
  -> invocation
  -> recovery
  -> think_tank_output_patch
  -> quality_check
```

## Repeatable Procedure

Claude Code 中的最小 runtime 必须按以下顺序执行：

1. 读取 `dispatch-contract.md`、`skill-mapping.md` 和本文。
2. 输出 `dispatch_request`。
3. 在调用任何工具前输出 `dispatch_decision`，并选择 `WebFetch`。
4. 调用一次 `WebFetch` 读取公开静态网页。
5. 将工具返回结果回收到 `runtime_result.sources[]` 和 `runtime_result.evidence[]`。
6. 如果调用失败，输出 `result_status: failed`，保持 `sources[]` 和 `evidence[]` 为空。
7. 输出 `boundaries[]` 和 `quality_check`。

这个 procedure 只证明 minimal runtime contract 可以被重复执行；在没有自动执行器和自动 recovery 证据前，不得声明完整 adapter runtime 已验证。

## Required Runtime Output

```yaml
runtime_result:
  runtime: claude-code-minimal
  mode: research
  profile: source-collector
  capability: source-acquisition
  dispatch_request: {}
  dispatch_decision: {}
  invocation: {}
  recovery: {}
  sources: []
  evidence: []
  boundaries: []
  quality_check: {}
```

## State Rules

```yaml
verified_partial_pre_invocation_decision:
  allowed_when:
    - dispatch_decision was printed before invocation
    - tool invocation succeeded
    - sources and evidence were produced
  not_enough_for:
    - full adapter runtime
    - automatic recovery contract

runtime_verified:
  requires:
    - repeatable runtime procedure
    - dispatch log generated from the procedure
    - recovery is not hand-written after the fact
    - failed invocation produces degraded or blocked state
```

## Failure Behavior

```yaml
failed_invocation:
  dispatch_log.invocation.result_status: failed
  dispatch_decision.status: dispatched
  recovery.result_recovered: false
  boundaries:
    - failure reason
    - fallback not executed unless actually attempted

no_available_skill:
  dispatch_decision.status: degraded
  invocation.invoked: false
  recovery.result_recovered: false
```

失败路径必须满足：

- 不生成 `sources[]`。
- 不生成 `evidence[]`。
- 不声称 fallback 已执行，除非确实有调用记录。
- 在 `boundaries[]` 中说明失败原因、未验证范围和未执行 fallback。

参考样例：

- `examples/claude-runtime-sample.json`：成功路径。
- `examples/claude-runtime-failure-sample.json`：失败/降级路径。

## Next Implementation Unit

最小实现单元应只覆盖：

```yaml
capability: source-acquisition
target_type: public_static_web
preferred_tool: WebFetch
fallback: none_for_v0_1_runtime
```

不要同时实现 Playwright、Obsidian、yt-dlp 或小红书。
