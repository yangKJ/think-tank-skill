# Capability Validation Roadmap

本文定义 v0.1 foundation 之后的 optional capability 验证顺序。

原则：一次只验证一个 capability，一次只验证一条低风险路径。

## 当前基线

```yaml
baseline:
  codex_foundation: verified
  claude_code_preflight: verified
  claude_code_source_acquisition: verified_partial_pre_invocation_decision
  full_adapter_runtime: not_verified
```

## 验证顺序

### 1. Source Acquisition

```yaml
capability: source-acquisition
priority: P0
status: verified_partial
next_goal: minimal_runtime_verified_after_repeatable_procedure
safe_scope:
  - public_static_web
  - readonly
  - no_login
  - no_download
blocked_scope:
  - dynamic_browser_dom
  - login_state
  - bulk_crawling
```

验收门槛：

- pre-invocation dispatch decision
- invocation log
- sources[]
- evidence[]
- boundaries[]
- failure path can degrade or block
- failure path does not fabricate sources or evidence

### 2. Browser Automation

```yaml
capability: browser-automation
priority: P1
status:
  codex_localhost: verified_optional
  codex_external_dom: blocked
  claude_code_playwright: planned
safe_scope:
  - public_page_dom_read
  - no_login
  - no_form_submit
blocked_scope:
  - authenticated_pages
  - purchase_or_submit_flows
  - social_media_scraping
```

### 3. Knowledge Persistence

```yaml
capability: knowledge-persistence
priority: P1
status:
  repository_markdown_artifact: verified
  obsidian_write: planned
safe_scope:
  - repository_markdown
  - examples_or_docs_artifact
blocked_scope:
  - private_vault_write_without_user_request
  - external_knowledge_graph_mutation
```

### 4. Media Processing

```yaml
capability: media-processing
priority: P2
status: planned
safe_scope:
  - user_provided_transcript
  - user_provided_summary
blocked_scope:
  - yt_dlp_download
  - whisper_transcription
  - copyrighted_media_bulk_processing
```

### 5. Social Listening

```yaml
capability: social-listening
priority: P3
status: planned
safe_scope:
  - user_provided_samples
  - manual_excerpt_analysis
blocked_scope:
  - xiaohongshu_scraping
  - login_or_cookie_flows
  - anti_bot_sensitive_collection
```

## 不变规则

- 不把 optional capability 写成 core dependency。
- 不把 skill installed 写成 skill verified。
- 不把 direct tool invocation 写成 adapter runtime。
- 不把 private write 当成默认行为。
