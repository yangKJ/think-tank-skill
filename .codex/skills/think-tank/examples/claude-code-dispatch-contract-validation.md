# Claude Code Dispatch Contract Validation

本文件记录 Claude Code 平台按 dispatch contract 执行 `source-acquisition` 最小验证的结果。

## 测试任务

```text
使用 think-tank research mode，按 Claude Code dispatch contract 执行一次 source-acquisition 最小验证。

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
status: dispatch_contract_verified_partial_order_gap
verified:
  - dispatch_request_output
  - dispatch_decision_output
  - dispatch_log_output
  - WebFetch_invoked
  - public_static_page_read
  - sources_output
  - evidence_output
not_verified:
  - dispatch_decision_before_invocation
  - adapter_auto_dispatch
  - result_recovery_without_manual_mapping
  - fallback_chain
  - web_access_wrapper_path
```

## Dispatch Request

```yaml
dispatch_request:
  mode: research
  profile: source-collector
  capability: source-acquisition
  task: 读取一个公开静态网页，将结果回收到 sources[] 和 evidence[]
  target: https://httpbin.org/html
  constraints:
    - readonly
    - no_login
    - no_download
    - no_private_write
    - no_social_media
  evidence_policy:
    network: allowed
    citations: optional
```

## Dispatch Decision

```yaml
dispatch_decision:
  selected_capability: source-acquisition
  candidate_skills:
    - web-access
    - WebFetch
    - google-ai-mode-skill
    - mcp-cli
  selected_skill: WebFetch
  selection_reason: 目标为公开静态网页，无需登录无需下载，WebFetch 是最小侵入性选择。
  invocation_method: WebFetch
  fallback_skills:
    - google-ai-mode-skill
    - chrome-devtools navigate_page
  risk_level: low
  status: dispatched
```

## Dispatch Log

```yaml
dispatch_log:
  started_at: "2026-05-14T20:28:00+08:00"
  invocation:
    invoked: true
    method: WebFetch
    target: https://httpbin.org/html
    result_status: success
  recovery:
    result_recovered: true
    recovered_as:
      - sources[0]
      - evidence[0]
  boundaries:
    - 仅验证 HTTP 200 静态页面
    - 未测试动态渲染
    - 未测试登录保护页面
    - 未测试 fallback 链
```

## Sources

```yaml
sources:
  - title: Herman Melville - Moby-Dick
    url: https://httpbin.org/html
    source_type: static-html
    summary: httpbin.org/html 返回一个简单 HTML 页面，内容为《白鲸》小说节选。
    reliability: medium
    freshness: "2026-05-14T20:28:00+08:00"
    extracted_at: "2026-05-14T20:28:05+08:00"
```

## Evidence

```yaml
evidence:
  - httpbin.org/html 是一个公开 HTTP 测试端点，返回固定 HTML 内容。
  - 页面标题为 Herman Melville - Moby-Dick，内容为《白鲸》小说节选。
  - 页面不包含 JavaScript 渲染，无登录态，无 cookie，无需认证。
  - WebFetch 成功提取了标题和正文内容。
```

## 结论

本次验证比前一次 direct WebFetch 更进一步：Claude Code 输出了 dispatch contract 要求的主要结构，并真实调用 WebFetch 获取公开静态页面。

但它仍不能升级为完整 adapter dispatch verified，原因是 Claude Code 明确指出：

```yaml
order_gap:
  dispatch_decision_before_invocation: false
  dispatch_decision_was_retrospective: true
```

因此当前状态应为：

```yaml
capability_auto_mapping: verified_partial_with_order_gap
adapter_dispatch_runtime: not_verified
result_recovery_contract: partial_manual_mapping
```

## 边界

本次验证基于用户粘贴的 Claude Code 输出归档；Codex 没有直接运行 Claude Code。

本次没有验证：

- 调用前预先形成 dispatch decision
- adapter 自动调度
- fallback
- web-access wrapper/CDP 路径
- 动态页面
- 登录页面
- 自动 result recovery

## 下一次通过条件

下一次若要提升状态，必须满足：

```yaml
required:
  - dispatch_decision 在 tool invocation 之前输出
  - dispatch_log 在 invocation 之后输出
  - sources[] 和 evidence[] 从 tool result 直接恢复
  - 输出明确 adapter_dispatch_path
  - 不把人工整理称为自动 recovery
```

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

