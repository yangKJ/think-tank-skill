# Claude Code Skill Mapping

本文定义 Claude Code 旧 skills 如何映射到 think-tank 能力槽。

这些 skills 是 Claude Code 平台可调用能力，不属于 think-tank core。其他平台可以用不同工具实现同样能力槽。

## 映射表

| Claude Code skill | think-tank capability | 说明 |
|-------------------|-----------------------|------|
| `web-access` | `source-acquisition` / `browser-automation` | 网页、动态页面、登录态、CDP 浏览器 |
| `playwright-cli` | `browser-automation` | 浏览器自动化和页面交互 |
| `google-ai-mode-skill` | `source-acquisition` | 带引用的快速网络研究 |
| `juejin-search` | `source-acquisition` | 技术社区和文章来源 |
| `36kr-hotlist` | `source-acquisition` | 科技和创业热点来源 |
| `xiaohongshu` | `social-listening` | 小红书内容和评论数据 |
| `social-media-analyzer` | `social-listening` | 社媒指标、互动率、ROI |
| `summarize` | `source-acquisition` / `media-processing` | URL、文件和视频摘要 |
| `yt-dlp` | `media-processing` | 视频下载和音频提取 |
| `openai-whisper` | `media-processing` | 本地音频转文字 |
| `xiaoyuzhou-transcribe` | `media-processing` | 小宇宙播客转录 |
| `pdf-extraction` | `source-acquisition` | PDF 文本、表格、元数据提取 |
| `obsidian` | `knowledge-persistence` | Markdown 知识库沉淀 |
| `notebooklm` | `knowledge-persistence` | 多源笔记本和生成报告 |
| `knowledge-graph-builder` | `knowledge-persistence` | 实体关系和知识图谱 |
| `taskflow` | `knowledge-persistence` | 长周期任务状态和恢复 |
| `mcp-cli` | `source-acquisition` | 动态发现和调用 MCP 工具 |

## 调用原则

1. 先由 think-tank 选择 mode、profile 和 capability。
2. 再由 Claude Code adapter 判断当前环境有哪些 skills 可用。
3. 优先使用任务最贴合、侵入性最低、可验证性最高的 skill。
4. skill 输出必须转换回 think-tank 的证据、角色观点或知识产物结构。
5. skill 不可用时，走 capability 的降级策略。

## 当前验证状态

```yaml
skill_discovery:
  status: verified
  evidence: think-tank/examples/claude-code-capability-discovery.md

capability_auto_mapping:
  status: verified_partial_pre_invocation_decision
  evidence: think-tank/examples/claude-code-dispatch-pre-invocation-validation.md
  limitation: 已验证 dispatch_decision 可在 WebFetch 调用前形成，但尚未验证完整 adapter runtime、自动 result recovery 或 fallback 链

external_skill_invocation:
  status: verified_partial_for_webfetch
  evidence: think-tank/examples/claude-code-external-source-readonly.md
  limitation: 通过直接 WebFetch 调用完成公开静态页读取，尚未验证完整 adapter 自动调度

next_candidate:
  - adapter_dispatch_for_web_access
  - playwright-cli_readonly_static_page
```

## 禁止行为

- 不把某个 Claude Code skill 写成协议必需依赖。
- 不把旧 research agent 的技能清单当成 think-tank 默认安装清单。
- 不把工具输出直接当最终结论。
- 不把平台私有路径写进 core。
