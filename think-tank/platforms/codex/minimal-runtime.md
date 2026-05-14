# Codex Minimal Runtime

本文定义 Codex 平台的最小 runtime mirror。

它的目的不是替代 Claude Code 的 `WebFetch`，而是在 Codex 主平台中验证同一套 think-tank runtime contract：

```text
dispatch_request
  -> dispatch_decision
  -> invocation
  -> recovery
  -> sources[]
  -> evidence[]
  -> boundaries[]
  -> quality_check
```

## Scope

```yaml
runtime: codex-minimal
capability: source-acquisition
profile: source-collector
target_type:
  - local_static_fixture
  - public_static_web_when_network_available
safe_constraints:
  - readonly
  - no_login
  - no_download
out_of_scope:
  - browser_dom_recovery
  - fallback_execution
  - private_write
  - social_media_scraping
```

## Reference Runner

参考实现：

```text
platforms/codex/runtime/source_acquisition_minimal.py
```

本 runner 支持：

- 本地静态 HTML fixture。
- `file://` 静态文件。
- 网络可用时的 `http` / `https` 公开静态网页。
- 失败路径边界输出。

## Status

```yaml
minimal_runtime_contract: implemented_as_repeatable_contract
codex_runtime_mirror: verified_with_local_fixture
source_acquisition_success_path: verified
source_acquisition_failure_path: verified
browser_external_dom: blocked
full_adapter_runtime: not_verified
```

## 不可过度声明

- 不得把本地 fixture 读取说成外部网页 DOM 读取。
- 不得把 `local_static_reader` 说成 Claude Code `WebFetch`。
- 不得把失败路径说成 fallback 已执行。
- 不得把 runtime mirror 说成完整多 agent runtime。
