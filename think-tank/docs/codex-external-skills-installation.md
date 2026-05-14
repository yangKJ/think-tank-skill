# Codex External Skills Installation

本文记录旧 research agent 工具型 skills 在 Codex 中的同级安装状态。

## 安装原则

```yaml
think_tank_position: peer_skill
external_skills_position: peer_skills
install_method: copy
core_rule: external_skills_are_not_inside_think_tank
think_tank_core_depends_on_peer_skills: false
```

`think-tank` 是高阶编排 Skill。旧 research agent 的其他 skills 是工具型能力，只能作为可选同级候选实现存在，不能成为 think-tank core 的依赖。

## 当前安装路径

```text
/Users/condy/Desktop/think-tank-skill/.codex/skills/
├── think-tank
├── web-access
├── xiaohongshu
└── ...
```

除 `think-tank` 外，这些 peer skills 是复制后的项目内副本，不是软链接。后续旧 research agent 目录删除后，当前项目仍然可用。

`think-tank` 本身使用仓库内软链接：

```text
.codex/skills/think-tank -> ../../think-tank
```

这保证 Codex 实际加载入口和主仓 `think-tank/` 是同一份内容，不产生双真相源。

旧 skill 的可执行入口必须指向当前项目本地路径，不能继续依赖 `~/.claude/skills` 或旧 `img-company/agents/research` 路径。历史 README 中若保留 Claude Code 安装说明，只能作为来源记录，不能作为 Codex 执行入口。

## 当前项目本地 peer skill 快照

```yaml
installed_optional_peer_skills:
  - 36kr-hotlist
  - apple-reminders
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
| domain workflow | `omni-research`、`research-workflow` |

## 状态边界

```yaml
external_peer_skills_are_optional: true
external_skills_snapshot_installed: verified
project_local_copy: true
codex_loader_refresh_required: true
external_skills_executable: not_verified
think_tank_can_reference_capability_mapping: verified
old_research_agent_shell_required: false
think_tank_core_depends_on_peer_skills: false
```

安装完成只证明：

- 当前项目 `.codex/skills/` 目录存在这些同级 skills。
- 每个已安装 skill 有 `SKILL.md`。
- think-tank 可以按 capability mapping 识别候选实现。
- think-tank 即使没有这些外部 peer skills，也必须能按核心协议降级运行。

安装完成不证明：

- 每个 skill 的脚本依赖都已满足。
- 每个 skill 都已适配 Codex。
- 登录态、MCP、API key、Chrome CDP、Obsidian vault 等环境已可用。
- think-tank 已完成所有外部 skills 端到端调用。
