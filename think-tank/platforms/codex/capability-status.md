# Codex Capability Status

本文定义 think-tank capabilities 在 Codex 主平台上的当前状态。

## 状态总览

```yaml
platform: codex
foundation_status: verified
default_execution: single_agent_multi_profile
last_updated: 2026-05-14
external_research_skills_installed: verified
external_research_skills_executable: not_verified
```

| capability | Codex 状态 | 默认实现 | 边界 |
|------------|------------|----------|------|
| `source-acquisition` | verified | 本地文件、用户提供材料、必要时 web | 最新外部信息需要显式联网验证 |
| `browser-automation` | verified_optional_localhost | Codex Browser localhost fixture | 外部网页 Browser 验证当前 blocked |
| `knowledge-persistence` | verified_for_markdown_artifact | 仓库内 Markdown artifact | 不默认写 Obsidian 或私有知识库 |
| `media-processing` | degraded_verified | 用户提供转录、摘要或本地材料 | 不默认下载、转码或转录媒体 |
| `social-listening` | degraded_verified | 用户提供样本或手动摘录 | 不默认抓取小红书、评论或社媒数据 |

## capability 判定流程

```text
用户任务
  -> 是否需要 capability
  -> 当前 Codex 是否有可用实现
  -> 是否需要用户授权或网络
  -> 执行或降级
  -> 回收证据
  -> 标注状态
```

## verified

当前已验证：

```yaml
source_acquisition:
  local_repository_collection: verified
  user_provided_material_analysis: verified
  external_readonly_web_source: verified

knowledge_persistence:
  repository_markdown_artifact: verified
  private_knowledge_base_write: planned

browser_automation:
  localhost_fixture: verified_optional
  external_web_readonly: blocked

degradation:
  media_processing_unavailable: verified
  social_listening_unavailable: verified
  knowledge_persistence_local_markdown_only: verified
  browser_automation_unavailable: verified
```

## planned

当前仍 planned：

```yaml
browser_automation_external_web: blocked
playwright_cli_integration: planned
yt_dlp_integration: planned
obsidian_integration: planned
xiaohongshu_integration: planned
true_multi_agent_execution: planned
claude_code_runtime: planned
```

## 同级 external skills

旧 research agent 的工具型 skills 已作为 Codex 同级 skills 安装。安装记录见：

```text
docs/codex-external-skills-installation.md
```

这会提升 think-tank 的可调度候选能力，但不改变状态边界：

```yaml
installed_not_equal_executable: true
capability_mapping_available: true
end_to_end_tool_invocation: per_skill_validation_required
```

## Codex 主平台策略

Codex 优先继续验证：

1. `browser-automation` 的只读外部网页路径。
2. `source-acquisition` 的外部来源只读路径。
3. 更严格的 artifact 索引和复用路径。

暂缓验证：

- 社媒抓取
- 视频下载
- 音频转录
- 私有知识库写入
- Claude Code subagent runtime
