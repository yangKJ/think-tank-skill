# Claude Code Dispatch Prompt

本文提供 Claude Code 中验证 adapter dispatch 的标准提示词。

使用场景：当需要验证 `source-acquisition`、`browser-automation` 等 capability 是否能经由 Claude Code adapter 映射到具体 skill/tool，并回收到 think-tank 输出结构时，使用本提示词。

## 标准提示词

```text
使用 think-tank research mode，按 Claude Code dispatch contract 执行一次 source-acquisition 最小验证。

任务：
读取一个公开、无需登录、无需下载的静态网页，并将结果回收到 sources[] 和 evidence[]。

目标 URL：
https://httpbin.org/html

请严格输出以下结构：

dispatch_request:
  mode:
  profile:
  capability:
  task:
  target:
  constraints:
  evidence_policy:

dispatch_decision:
  selected_capability:
  candidate_skills:
  selected_skill:
  selection_reason:
  invocation_method:
  fallback_skills:
  risk_level:
  status:

dispatch_log:
  started_at:
  dispatch_request:
  dispatch_decision:
  invocation:
    invoked:
    method:
    target:
    result_status:
  recovery:
    result_recovered:
    recovered_as:
  boundaries:

sources:
  - title:
    url:
    source_type:
    summary:
    reliability:
    freshness:
    extracted_at:

evidence:
  - ""

boundaries:
  - ""

verified:
  - ""

not_verified:
  - ""

要求：
- 必须先读取 think-tank/platforms/claude-code/dispatch-contract.md
- 必须读取 think-tank/platforms/claude-code/skill-mapping.md
- 只读公开网页
- 不登录
- 不下载文件
- 不抓社媒
- 不写入 Obsidian 或私有知识库
- 如果没有输出 dispatch_decision 和 dispatch_log，不得标记为 adapter dispatch verified
- 如果仍是直接调用 WebFetch，必须标记为 verified_partial
```

## 通过标准

```yaml
pass:
  - dispatch_request_present
  - dispatch_decision_present
  - dispatch_log_present
  - selected_skill_present
  - invocation_result_present
  - sources_present
  - evidence_present
  - boundaries_present
  - no_overclaim
```

## 失败标准

```yaml
fail:
  - no_dispatch_decision
  - no_dispatch_log
  - direct_tool_call_claimed_as_full_adapter_dispatch
  - missing_sources
  - missing_evidence
  - missing_boundaries
  - unsafe_operation_attempted
```

