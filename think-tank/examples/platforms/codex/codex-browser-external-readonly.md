# Codex Browser External Readonly Validation

本文记录 Codex 主平台对外部只读 browser-automation 的真实验证结果。

## 测试任务

```text
使用 Playwright 打开一个公开外部网页，读取 URL、标题、H1 和首段正文，验证 browser-automation 是否可以作为 optional capability 回收外部网页 DOM 证据。
```

## 执行声明

```yaml
platform: codex
capability: browser-automation
implementation: playwright_cli_with_headless_chrome
target: https://example.com
status: verified_partial
dispatch_decision:
  route_selected: browser-automation
  provider_selected: playwright-cli
  reason: external readonly DOM recovery required
invoked_providers:
  - playwright-cli
not_invoked_providers:
  - web-access
  - taskflow
verified:
  - external_browser_launch
  - external_dom_read
  - external_page_result_recovery
  - title_h1_paragraph_capture
not_verified:
  - login_state
  - click_interaction
  - form_submission
  - javascript_heavy_app_flow
  - authenticated_browser_session
```

## Invocation Log

```yaml
steps:
  - launch headless Chrome through Playwright
  - navigate to https://example.com with domcontentloaded
  - recover URL, title, first H1 and first paragraph
  - close browser after readonly capture
```

## 回收结果

```yaml
source:
  url: https://example.com/
  title: Example Domain
  source_type: public_web
  summary: 页面说明 example.com 可用于文档示例，无需额外许可。
evidence:
  h1: Example Domain
  first_paragraph: This domain is for use in documentation examples without needing permission. Avoid use in operations.
recovery:
  sources[]: recovered
  evidence[]: recovered
  snapshot: not_persisted
```

## 结果判断

`playwright-cli` 已经形成一条真实 external browser readonly 证据，因此当前可以把 Codex 的 browser-automation 外部只读路径提升到 `verified_partial`。

这仍然只是 optional capability，不构成“通用浏览器自动化已稳定”的声明。

## 行动建议

1. 将 `playwright-cli` 的公开状态更新为 external readonly `verified_partial`。
2. 保持登录态、点击交互、动态复杂页面和表单提交为未验证边界。
3. stable gate 后续继续关注多 agent 和 long-running lifecycle，而不是再把 browser external readonly 记成 blocked。

## 边界

本次没有使用登录态，没有执行点击，没有写外部状态，没有验证动态前端应用，也没有验证 Browser pane UI 交互。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```
