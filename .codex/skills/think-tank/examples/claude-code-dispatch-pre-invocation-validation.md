# Claude Code Dispatch Pre Invocation Validation

本文件记录 Claude Code 平台对 dispatch contract 中“先决策、后调用”要求的验证结果。

## 测试任务

```text
使用 think-tank research mode，按 Claude Code dispatch contract 执行 source-acquisition 最小验证。

目标 URL：
https://httpbin.org/html
```

## 执行声明

```yaml
platform: claude-code
mode: research
profile: source-collector
capability: source-acquisition
selected_skill: WebFetch
target: https://httpbin.org/html
status: verified_partial_pre_invocation_decision
verified:
  - dispatch_request_output_before_invocation
  - dispatch_decision_output_before_invocation
  - WebFetch_invoked_after_decision
  - dispatch_log_output_after_invocation
  - sources_output
  - evidence_output
not_verified:
  - full_adapter_runtime
  - automatic_result_recovery_contract
  - fallback_chain_execution
  - web_access_wrapper_path
  - subagent_runtime
```

## Dispatch Request

```yaml
dispatch_request:
  mode: research
  profile: source-collector
  capability: source-acquisition
  task: 读取公开静态网页 HTML 内容
  target: https://httpbin.org/html
  constraints:
    - readonly
    - no_login
    - no_download
    - no_private_write
    - no_social_media
    - no_obsidian_write
    - public_only
  evidence_policy:
    network: allowed
    citations: optional
```

## Dispatch Decision

该部分在 WebFetch 调用前输出。

```yaml
dispatch_decision:
  selected_capability: source-acquisition
  candidate_skills:
    - web-access
    - WebFetch
    - google-ai-mode-skill
    - mcp-cli
  selected_skill: WebFetch
  selection_reason: 目标为公开静态网页，仅需读取 HTML 源码。WebFetch 是最低侵入性选择。
  invocation_method: WebFetch
  fallback_skills:
    - web-access
    - google-ai-mode-skill
  risk_level: low
  status: planned
```

## Invocation

```yaml
invocation:
  tool: WebFetch
  target: https://httpbin.org/html
  result: 200 OK
  bytes: 3.7KB
```

## Dispatch Log

```yaml
dispatch_log:
  started_at: "2026-05-14 20:38:00 GMT+8"
  invocation:
    invoked: true
    method: WebFetch
    target: https://httpbin.org/html
    result_status: success
  recovery:
    result_recovered: true
    recovered_as:
      - sources[]
      - evidence[]
  boundaries:
    - 静态公开网页，无需登录
    - 仅验证 dispatch_decision 先于 invocation
    - 不执行 fallback 测试
    - 不写入 Obsidian
```

## Sources

```yaml
sources:
  - title: Herman Melville - Moby-Dick
    url: https://httpbin.org/html
    source_type: static-html
    summary: 船上的老铁匠 Perth 在甲板上修理武器，隐藏着失去双足和被抢劫的悲剧过去。
    reliability: medium
    freshness: "2026-05-14"
    extracted_at: "2026-05-14 20:38:02 GMT+8"
```

## Evidence

```yaml
evidence:
  - dispatch_decision 于 WebFetch 调用前完整输出，未事后补写。
  - WebFetch 成功返回页面内容，标题为 Herman Melville - Moby-Dick。
  - result_recovered 映射到 sources[] 结构。
```

## 结论

本次验证通过了前一轮缺失的关键顺序要求：

```yaml
dispatch_decision_pre_invocation: confirmed
```

因此可以将 Claude Code 的 capability auto mapping 状态从 `mock` 提升为：

```yaml
capability_auto_mapping: verified_partial_pre_invocation_decision
```

但仍不能标记为完整 adapter runtime：

```yaml
adapter_dispatch_runtime: not_verified
result_recovery_contract: partial_manual_mapping
```

## 边界

本次验证基于用户粘贴的 Claude Code 输出归档；Codex 没有直接运行 Claude Code。

本次没有验证：

- 完整 think-tank adapter runtime
- 自动 result recovery contract
- fallback 链
- web-access wrapper/CDP 路径
- subagent runtime

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

