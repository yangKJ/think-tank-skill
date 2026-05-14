# Codex External Skills Installation

本文记录旧 research agent 工具型 skills 在 Codex 中的同级安装状态。

## 安装原则

```yaml
think_tank_position: peer_skill
external_skills_position: peer_skills
install_method: symlink
core_rule: external_skills_are_not_inside_think_tank
```

`think-tank` 是高阶编排 Skill。旧 research agent 的其他 skills 是工具型能力，必须和 `think-tank` 同级安装。

## 当前安装路径

```text
/Users/condy/.codex/skills/
├── think-tank -> /Users/condy/Desktop/think-tank-skill/think-tank
├── web-access -> /Users/condy/Desktop/img-company/agents/research/.claude/skills/web-access
├── xiaohongshu -> /Users/condy/Desktop/img-company/agents/research/.claude/skills/xiaohongshu
└── ...
```

## 已安装旧 research skills

```yaml
installed_external_skills:
  - 36kr-hotlist
  - apple-reminders
  - competitor_analysis
  - google-ai-mode-skill
  - juejin-search
  - knowledge-graph-builder
  - mcp-cli
  - notebooklm
  - obsidian
  - omni-research
  - openai-whisper
  - pdf-extraction
  - playwright-cli
  - research-workflow
  - social-media-analyzer
  - stable-diffusion-image-generation
  - summarize
  - taskflow
  - using-tmux-for-interactive-commands
  - vision-analysis
  - web-access
  - xiaohongshu
  - xiaoyuzhou-transcribe
  - yt-dlp
```

`think-tank` 也已安装，但它来自当前主仓，不使用旧 research 的 `think-tank`。

## Capability Mapping

| Capability | 已安装同级 skills |
|------------|-------------------|
| `source-acquisition` | `web-access`、`google-ai-mode-skill`、`juejin-search`、`36kr-hotlist`、`pdf-extraction`、`mcp-cli`、`summarize` |
| `browser-automation` | `web-access`、`playwright-cli` |
| `social-listening` | `xiaohongshu`、`social-media-analyzer` |
| `media-processing` | `yt-dlp`、`openai-whisper`、`xiaoyuzhou-transcribe`、`summarize`、`vision-analysis` |
| `knowledge-persistence` | `obsidian`、`notebooklm`、`knowledge-graph-builder`、`taskflow` |
| out-of-core optional | `apple-reminders`、`stable-diffusion-image-generation`、`using-tmux-for-interactive-commands` |
| domain workflow | `competitor_analysis`、`omni-research`、`research-workflow` |

## 状态边界

```yaml
external_skills_installed: verified
codex_loader_refresh_required: true
external_skills_executable: not_verified
think_tank_can_reference_capability_mapping: verified
old_research_agent_shell_required: false
```

安装完成只证明：

- Codex skills 目录存在这些同级 skills。
- 每个已安装 skill 有 `SKILL.md`。
- think-tank 可以按 capability mapping 识别候选实现。

安装完成不证明：

- 每个 skill 的脚本依赖都已满足。
- 每个 skill 都已适配 Codex。
- 登录态、MCP、API key、Chrome CDP、Obsidian vault 等环境已可用。
- think-tank 已完成所有外部 skills 端到端调用。

