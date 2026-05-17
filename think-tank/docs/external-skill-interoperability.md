# External Skill Interoperability

think-tank 是高阶编排 Skill，不复制外部工具型 skill。

本文定义旧 research agent 里的外部 skills 如何与 think-tank 共存。

## 原则

1. capability 描述“需要什么能力”，不是“必须用哪个工具”。
2. 外部 skill 可用时由平台 adapter 调用。
3. 外部 skill 不可用时走 capability 降级路径。
4. 不能因为某个旧 skill 很强，就把它写进 core protocol。
5. 高风险工具必须默认后置，不能在 minimal install 场景阻断 think-tank。

## 分类

### Core Capability Candidates

这些旧 skills 可以作为 capability 候选实现：

| Capability | 候选外部 skills |
|------------|------------------|
| `source-acquisition` | `agent-reach`、`web-access`、`google-ai-mode-skill`、`juejin-search`、`36kr-hotlist`、`pdf-extraction`、`mcp-cli`、`summarize` |
| `browser-automation` | `web-access`、`playwright-cli` |
| `social-listening` | `xiaohongshu`、`social-media-analyzer` |
| `media-processing` | `yt-dlp`、`openai-whisper`、`xiaoyuzhou-transcribe`、`summarize`、`vision-analysis` |
| `knowledge-persistence` | `obsidian`、`notebooklm`、`knowledge-graph-builder`、`taskflow` |

### Mode Orchestration Sources

这些旧 skills 的价值是流程，不是工具：

| 旧 skill | 新抽象 |
|----------|--------|
| `research-workflow` | 旧 route wrapper 已删除；研究深度进入 `modes/research.md`，Codex 触发迁移到 provider policy |
| `omni-research` | `research_depth: autonomous_research` |
| `think-tank` | `council mode`、`research mode` 和 runtime contracts |

### Out-of-Core Optional Skills

这些旧 skills 不属于 think-tank core，但可以被某个平台或用户环境作为外部工具使用：

| 旧 skill | 原因 |
|----------|------|
| `agent-reach` | 统一 source-acquisition 入口，不承担真实抓取，而是做能力路由 |
| `apple-reminders` | 个人提醒和系统 App 操作，不是 think-tank 研究协议 |
| `stable-diffusion-image-generation` | 生成图片，不是信息收集或审议协议本身 |
| `using-tmux-for-interactive-commands` | 平台执行辅助，不是 think-tank capability |

## Minimal Install 行为

只安装 think-tank、没有任何外部 skill 时，think-tank 仍必须可用：

```yaml
source-acquisition: user_input_or_local_context
browser-automation: unavailable_with_boundary
social-listening: user_provided_sample_analysis
media-processing: user_provided_transcript_or_summary
knowledge-persistence: markdown_artifact
```

## 状态

```yaml
external_skills_required_for_core: false
old_research_skills_all_classified: true
minimal_install_supported: true
full_external_tool_runtime_verified: false
```
