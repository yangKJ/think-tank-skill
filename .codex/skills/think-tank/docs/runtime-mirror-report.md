# Runtime Mirror Report

本文记录 think-tank minimal runtime 在 Codex 与 Claude Code 之间的当前镜像状态。

## 结论

```yaml
codex_minimal_runtime:
  status: verified_with_local_fixture
  success_path: verified
  failure_path: verified
  runner: platforms/codex/runtime/source_acquisition_minimal.py

claude_code_minimal_runtime:
  status: verified_partial_with_success_pre_invocation_and_failure_degradation
  success_sample: examples/claude-runtime-sample.json
  failure_sample: examples/claude-runtime-failure-sample.json
  final_validation_prompt: platforms/claude-code/final-validation-prompt.md
  final_validation_record: examples/claude-code-final-validation.md

cross_platform_contract:
  protocol_shape: aligned
  runtime_result_shape: aligned
  adapter_execution: platform_specific
```

## 对齐字段

两个平台都必须输出：

- `runtime`
- `mode`
- `profile`
- `capability`
- `dispatch_request`
- `dispatch_decision`
- `invocation`
- `recovery`
- `sources[]`
- `evidence[]`
- `boundaries[]`
- `quality_check`

## 差异字段

```yaml
codex:
  invocation.method: local_static_reader
  verified_by: repo fixture execution

claude_code:
  invocation.method: WebFetch
  verified_by: low-flow Claude Code validation record
  caveat: failure path pre-invocation ordering is not confirmed from transcript
```

## 边界

- Codex fixture 成功不等于外部网页 DOM 成功。
- Claude Code WebFetch 成功不等于完整 adapter runtime。
- 两个平台都不默认执行 fallback。
- 两个平台都不默认执行 private write、media download 或 social scraping。
