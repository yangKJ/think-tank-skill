# Skill Router

本文定义 think-tank 如何把 capability slots 解析成 optional peer skills。

skill-router 是“连接技能的中间件”，但它不是工具 skill，也不是某个平台的脚本。它只产生路由决策。

## Input

```yaml
selected_intent: ""
selected_recipe: ""
selected_mode: ""
selected_profiles: []
selected_capabilities: []
task_constraints: []
available_peer_skills: []
```

## Output

```yaml
skill_route:
  capability: ""
  required: true | false
  candidate_peer_skills: []
  selected_peer_skill: "" | null
  selection_reason: ""
  dispatch_allowed: true | false
  fallback: core_protocol | user_materials | local_files | ask_user | stop
```

## Resolution Flow

```text
recipe.optional_peer_skills
  + capability candidate skills
  + platform available skills
  + task constraints
  -> ranked candidate list
  -> selected_peer_skill or fallback
```

## Ranking Rules

1. 安全性优先：只读、无登录、无私有写入优先。
2. 任务匹配优先：候选 skill 必须服务当前 capability。
3. 最小能力优先：静态资料优先简单读取，不直接上重型浏览器或下载工具。
4. 可回收性优先：输出能映射到 `sources[]`、`evidence[]`、`role-result` 的 skill 优先。
5. 已验证优先：本平台本仓已验证过的 peer skill 优先。
6. 用户授权优先：登录、下载、写入私有库、社媒抓取必须有明确授权。

## Capability Candidate Map

```yaml
source-acquisition:
  candidates:
    - web-access
    - summarize
    - google-ai-mode-skill
    - juejin-search
    - 36kr-hotlist
    - pdf-extraction
    - mcp-cli
  fallback:
    - user_provided_materials
    - local_files
    - model_reasoning_with_boundaries

browser-automation:
  candidates:
    - web-access
    - playwright-cli
  fallback:
    - static_fetch
    - user_provided_screenshots
    - describe_unverified_dynamic_behavior

social-listening:
  candidates:
    - xiaohongshu
    - social-media-analyzer
  fallback:
    - pasted_social_samples
    - exported_comments
    - no_social_claims

media-processing:
  candidates:
    - yt-dlp
    - openai-whisper
    - xiaoyuzhou-transcribe
    - summarize
    - vision-analysis
  fallback:
    - user_provided_transcript
    - user_provided_summary
    - metadata_only

knowledge-persistence:
  candidates:
    - obsidian
    - notebooklm
    - knowledge-graph-builder
    - taskflow
  fallback:
    - repository_markdown_artifact
    - inline_summary
    - no_private_write
```

## Recipe Overrides

recipe 可以缩小或排序候选 skill，但不能新增硬依赖。

示例：

```yaml
competitive-intelligence:
  source-acquisition:
    prefer:
      - competitor_analysis
      - web-access
      - juejin-search
      - summarize
  social-listening:
    prefer:
      - xiaohongshu
      - social-media-analyzer
```

`competitor_analysis` 可以作为竞品分析 recipe 的优先候选，但它仍是 optional peer skill。

## Decision Example

```yaml
selected_intent: competitive_intelligence
selected_recipe: competitive-intelligence
selected_capabilities:
  - source-acquisition
  - social-listening

skill_routes:
  - capability: source-acquisition
    required: true
    candidate_peer_skills:
      - competitor_analysis
      - web-access
      - summarize
    selected_peer_skill: competitor_analysis
    selection_reason: "任务是竞品分析，competitor_analysis 是最贴近的可选 peer skill"
    dispatch_allowed: true
    fallback: core_protocol

  - capability: social-listening
    required: false
    candidate_peer_skills:
      - xiaohongshu
      - social-media-analyzer
    selected_peer_skill: null
    selection_reason: "未获得登录/抓取授权，降级为用户提供样本"
    dispatch_allowed: false
    fallback: user_materials
```

## Anti-Patterns

- `竞品分析` 直接等于调用 `competitor_analysis`。
- `xiaohongshu` 已安装就默认抓取社媒内容。
- `obsidian` 已安装就默认写用户私有库。
- `yt-dlp` 已安装就默认下载视频。
- route 失败时伪造 sources 或 evidence。
