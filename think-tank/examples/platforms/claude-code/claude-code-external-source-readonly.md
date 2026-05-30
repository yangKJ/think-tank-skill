# Claude Code External Source Readonly

本文件记录 Claude Code 平台对 `source-acquisition` 的低风险外部只读验证。

## 测试任务

```text
使用 think-tank research mode，通过 Claude Code 中已安装的 web-access 或 playwright-cli，对一个公开、无需登录、无需下载的静态网页做只读获取测试，并验证结果是否能回收到 think-tank 的 evidence/sources 结构。
```

## 执行声明

```yaml
platform: claude-code
mode: research
execution_method: direct_skill_tool_invocation
selected_profiles:
  - source-collector
selected_capabilities:
  - source-acquisition
selected_skill: web-access
skill_invocation_method: WebFetch
target: https://httpbin.org/html
capability_status: verified_partial
result_recovered: partial
evidence_format:
  - source-acquisition.sources[]
  - think-tank.output.evidence[]
verified:
  - public_static_page_read
  - no_login_required
  - no_download
  - result_mapped_to_sources_shape
  - result_mapped_to_evidence_shape
not_verified:
  - full_adapter_auto_dispatch
  - profile_to_capability_runtime_chain
  - capability_fallback_runtime
  - structured_result_recovery_contract
  - browser_dom_interaction
status: external_source_readonly_verified_partial
```

## 回收证据

```yaml
source:
  title: Sample HTML Page - httpbin.org
  url: https://httpbin.org/html
  source_type: web
  summary: HTTPBIN 提供随机 HTML 样本页，用于测试 HTTP 客户端
  reliability: medium
  freshness: "2026-05-14"
  extracted_at: "2026-05-14T18:00:00+08:00"
```

映射到 `source-acquisition`：

```yaml
sources:
  - title: Sample HTML Page - httpbin.org
    url: https://httpbin.org/html
    source_type: web
    summary: HTTPBIN 提供随机 HTML 样本页，用于测试 HTTP 客户端
    reliability: medium
    freshness: "2026-05-14"
    extracted_at: "2026-05-14T18:00:00+08:00"
gaps: []
```

映射到 think-tank output：

```yaml
evidence:
  - https://httpbin.org/html — HTTPBIN 随机 HTML 样本，reliability=medium，source_type=web
```

## 结论

Claude Code 可以通过 `web-access`/`WebFetch` 对公开静态网页做只读获取，并能将结果手动映射到 think-tank 的 `sources[]` 和 `evidence[]` 结构。

这证明了低风险外部 source acquisition 的工具层可用性，但还没有证明 think-tank adapter 的完整自动调度链路。

## 通过项

```yaml
pass:
  public_web_read: true
  no_auth: true
  no_download: true
  source_shape_mapping: true
  evidence_shape_mapping: true
  no_adapter_overclaim: true
```

## 缺口

```yaml
gaps:
  full_adapter_auto_dispatch: not_verified
  source_collector_runtime_invocation: not_verified
  fallback_from_web_access_to_playwright: not_verified
  result_recovery_contract: partial_manual_mapping
  browser_automation_dom_read: not_tested
```

## 边界

本次验证基于用户粘贴的 Claude Code 输出归档；Codex 没有直接运行 Claude Code。

本次没有登录、没有下载、没有抓取社媒、没有写入 Obsidian，也没有验证 Playwright 或 Browser DOM 交互。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

