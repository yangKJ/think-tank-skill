# Claude Code Dispatch Contract Sample

本文件给出 Claude Code adapter dispatch 的目标输出样例。

它不是运行时验证结果，而是下一次 Claude Code 验证必须满足的输出形态。

## Dispatch Request

```yaml
dispatch_request:
  mode: research
  profile: source-collector
  capability: source-acquisition
  task: 读取公开静态网页并回收 evidence
  target: https://httpbin.org/html
  constraints:
    - readonly
    - no_login
    - no_download
    - no_private_write
  evidence_policy:
    network: allowed
    citations: required
```

## Dispatch Decision

```yaml
dispatch_decision:
  selected_capability: source-acquisition
  candidate_skills:
    - web-access
    - google-ai-mode-skill
    - mcp-cli
  selected_skill: web-access
  selection_reason: 公开静态网页只读获取，优先使用低风险网页读取能力
  invocation_method: WebFetch
  fallback_skills:
    - google-ai-mode-skill
    - mcp-cli
  risk_level: low
  status: dispatched
```

## Dispatch Log

```yaml
dispatch_log:
  started_at: "2026-05-14T00:00:00+08:00"
  dispatch_request:
    capability: source-acquisition
    target: https://httpbin.org/html
  dispatch_decision:
    selected_skill: web-access
    invocation_method: WebFetch
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
    - 未验证登录态页面
    - 未验证动态 DOM
    - 未验证 fallback
```

## Sources

```yaml
sources:
  - title: Sample HTML Page - httpbin.org
    url: https://httpbin.org/html
    source_type: web
    summary: HTTPBIN HTML sample page for HTTP client testing
    reliability: medium
    freshness: "2026-05-14"
    extracted_at: "2026-05-14T00:00:00+08:00"
gaps: []
```

## Evidence

```yaml
evidence:
  - https://httpbin.org/html — HTTPBIN HTML sample page, reliability=medium, source_type=web
```

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

