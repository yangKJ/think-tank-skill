# Codex Research Agent Takeover Test Plan

本文定义 Codex 用 `think-tank + 同级 external skills` 接管旧 research agent 能力的测试顺序。

## 当前结构

```yaml
orchestrator_skill: think-tank
tool_skills: peer Codex skills
old_research_agent_shell_required: false
```

## 测试原则

1. 先验证低风险只读能力。
2. 一次只验证一个 capability。
3. installed 不等于 executable。
4. 不登录、不下载、不写私有知识库，除非用户明确授权。
5. 每次验证都输出 `execution_method`、`capability_status`、`sources/evidence`、`boundaries`。

## 阶段 1：本地研究接管

目标：证明 Codex 可以用 think-tank 在本仓执行旧 research agent 的研究组织能力。

```yaml
mode: research
capabilities:
  - source-acquisition
  - knowledge-persistence
skills_used:
  - think-tank
scope:
  - local repository
  - markdown artifacts
status: ready
```

测试 prompt：

```text
用 think-tank research mode 研究：
当前 think-tank 主仓是否已经具备接管旧 research agent 的能力？
只使用本地仓库资料，输出结论、依据、分歧、风险、行动建议和边界。
```

## 阶段 2：低风险外部来源

目标：验证 source-acquisition 候选 skills 的只读路径。

优先级：

1. `36kr-hotlist`
2. `juejin-search`
3. `google-ai-mode-skill`
4. `web-access`
5. `pdf-extraction`

边界：

- 只读。
- 不登录。
- 不批量抓取。
- 不把 skill installed 写成 verified。

## 阶段 3：媒体与文档

目标：验证用户提供材料或公开样本的处理。

候选：

- `summarize`
- `yt-dlp`
- `openai-whisper`
- `xiaoyuzhou-transcribe`
- `vision-analysis`

默认先用用户提供 transcript/summary，不直接下载或转录媒体。

## 阶段 4：知识沉淀

目标：先验证仓库内 Markdown artifact，再考虑私有知识库。

候选：

- `obsidian`
- `notebooklm`
- `knowledge-graph-builder`
- `taskflow`

默认不写 Obsidian vault。

## 阶段 5：社媒舆情

目标：先验证用户提供样本分析，再考虑小红书真实工具链。

候选：

- `xiaohongshu`
- `social-media-analyzer`

默认不使用登录态、不抓取评论、不处理反爬敏感流程。

## 当前接管状态

```yaml
codex_peer_skills_installed: verified
think_tank_orchestrator_installed: verified
old_research_agent_shell_required: false
local_research_takeover: ready
external_tool_takeover: requires_per_skill_validation
```

