# Codex External Source Validation

本文件记录 Codex 主平台对外部只读 `source-acquisition` 的最小验证。

## 测试任务

```text
用 think-tank research mode 验证：
Codex 是否可以读取一个公开、无需登录、无需交互的外部网页来源，并将结果作为 evidence 回收到 think-tank 输出。
```

## 执行声明

```yaml
platform: codex
execution_method: single_agent_multi_profile
mode: research
capabilities:
  - source-acquisition
implementation: codex_web_open
target: https://example.com
external_skills_invoked: false
browser_automation_invoked: false
verified:
  - external_readonly_source_open
  - title_and_body_text_recovery
  - citation_available
not_verified:
  - browser_dom_interaction
  - login_state
  - javascript_heavy_page
  - form_submission
  - playwright_cli
```

## 回收证据

```yaml
source:
  title: Example Domain
  url: https://example.com/
  source_type: public_web
  summary: 该页面说明 example.com 可用于文档示例，不需要许可。
  reliability: high
  freshness: stable_reference_page
```

## 结论

Codex 可以在不调用 Browser automation 的情况下，对公开、静态、无需登录的网页做只读 source acquisition，并把标题、正文摘要和 URL 回收到 think-tank 输出。

这验证的是 `source-acquisition`，不是 `browser-automation`。

## 角色观点

```yaml
source_collector:
  claim: 公开静态网页可以作为 Codex source-acquisition 的外部来源。
  confidence: high

skeptic:
  claim: 该验证不能外推到动态页面、登录态页面、点击交互或 DOM 级浏览器自动化。
  confidence: high

report_architect:
  claim: 外部来源回收结果必须记录 target、implementation、verified 和 not_verified。
  confidence: high
```

## 分歧与风险

- 分歧：是否把该能力归入 browser-automation。
- 判断：不归入。它只证明 Codex web 只读来源获取，不证明 Browser 或 Playwright。
- 风险：用户可能把 web open 与 Browser automation 混淆。
- 缓解：在 capability status 中分别标注 `external_source_readonly` 和 `browser_external_readonly`。

## 行动建议

1. 将 `external_source_readonly` 标为 Codex verified。
2. 继续将 Browser 外部只读路径标为 blocked 或 planned，直到 in-app Browser pane 可用并真实回收 DOM。
3. 后续真实调研任务可以优先使用 source-acquisition，再按需要升级到 Browser automation。

## 边界

本次没有使用 Browser automation，没有点击页面，没有处理登录态，没有验证动态 DOM，也没有调用外部技能。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

