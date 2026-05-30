# Claude Code Adapter Dispatch Attempt

本文件记录 Claude Code 平台对 `source-collector -> source-acquisition -> adapter -> WebFetch` 链路的验证尝试。

## 测试任务

```text
使用 think-tank research mode，验证 source-collector profile 是否能按 think-tank 协议选择 source-acquisition capability，并由 Claude Code adapter 映射到 web-access/WebFetch，对公开静态网页做只读获取，最后自动输出 sources[] 和 evidence[]。
```

## 执行声明

```yaml
platform: claude-code
mode: research
execution_method: direct_webfetch_after_protocol_selection
selected_profiles:
  - source-collector
selected_capabilities:
  - source-acquisition
selected_skill: WebFetch
skill_invocation_method: direct invocation
adapter_dispatch_path: not_executed
capability_status: verified_partial
result_recovered: true
evidence_format:
  - sources[]
verified:
  - source_collector_profile_selected
  - source_acquisition_capability_selected
  - WebFetch_read_public_pages
  - sources_shape_output
  - constraints_respected
not_verified:
  - adapter_dispatch_mechanism
  - capability_to_skill_to_tool_full_chain
  - automatic_result_recovery_contract
  - fallback_runtime_behavior
status: adapter_dispatch_not_executed_verified_partial
```

## 执行记录

Claude Code 执行了公开只读获取：

```yaml
fetches:
  - url: https://developer.apple.com/documentation/coreimage
    result: "200 OK"
    bytes: "3.2KB"
  - query: "Apple Core Image CIContext Metal performance 2024"
    result: "0 searches"
  - url: https://developer.apple.com/metal/apple-ml/
    result: "404 Not Found"
    bytes: "0"
  - url: https://www.apple.com/macos/
    result: "200 OK"
    bytes: "230.1KB"
```

## 结论

本次验证证明：

- `source-collector` profile 可以被选择。
- `source-acquisition` capability 可以被选择。
- Claude Code 可以直接调用 WebFetch 读取公开网页。
- 输出可以整理为 `sources[]` 形态。

本次没有证明：

- Claude Code adapter 自动完成 capability 到 skill 的调度。
- profile 到 capability 到 adapter 到 skill 到 evidence 的完整链路。
- fallback 或结果回收契约。

## 关键发现

当前实际路径：

```text
think-tank protocol: source-collector + source-acquisition
  -> capability selected
  -> direct WebFetch invocation
  -> sources[] output
```

预期 adapter 路径：

```text
think-tank protocol: source-collector + source-acquisition
  -> capability auto-mapping
  -> Claude Code adapter selects web-access/WebFetch
  -> adapter dispatch
  -> skill/tool output
  -> sources[] and evidence[] recovery
```

差异：

```yaml
adapter_dispatch:
  expected: true
  actual: false
  status: not_verified
```

## 约束检查

```yaml
readonly_public_web: pass
no_login: pass
no_download: pass
no_social_scraping: pass
no_obsidian_write: pass
```

## 行动建议

1. 将本次记录为 adapter dispatch attempt，而不是 full adapter verified。
2. 当时保持 `capability_auto_mapping: mock`；后续 pre-invocation 验证已将其提升为 `verified_partial_pre_invocation_decision`。
3. 保持 `external_source_readonly: verified_partial`。
4. 若要继续推进，需要实现或明确 Claude Code adapter dispatch 机制，而不是继续手动调用 WebFetch。

## 边界

本次验证基于用户粘贴的 Claude Code 输出归档；Codex 没有直接运行 Claude Code。

本次读取了公开网页，但没有登录、下载、抓社媒、写私有知识库，也没有验证自动调度。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```
