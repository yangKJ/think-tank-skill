# Skill Router

本文定义 think-tank 如何把 capability slots 解析成可用的能力提供者。

skill-router 是“连接能力的中间件”，但它不是工具 skill，也不是某个平台的脚本。它只产生路由决策。

核心原则：

- 主协议不写死任何具体 skill 名。
- router 只认识 capability、provider descriptor、约束和降级策略。
- 具体 skill 名必须来自当前平台 adapter 的运行时发现结果，或来自项目本地 registry。
- 没有任何外部 provider 时，think-tank 仍必须能按 core protocol 运行。

## Input

```yaml
selected_intent: ""
selected_recipe: ""
selected_mode: ""
selected_profiles: []
selected_capabilities: []
task_constraints: []
available_providers: []
```

`available_providers` 由平台 adapter 提供，不由 protocol 或 router 内置。

每个 provider 至少应描述：

```yaml
provider:
  id: ""                    # 平台内唯一标识，可是 skill 名、tool 名、脚本名或服务名
  platform: ""              # codex | claude-code | local | remote | other
  capabilities: []          # 可服务的 capability slots
  access_level: readonly | write | network | private | privileged
  requires_permission: true | false
  recovery_targets: []      # sources | evidence | role_result | artifact | boundary_only
  status: available | unavailable | blocked | unknown
  verification: verified | partial | mock | tracking | planned | unknown
```

## Output

```yaml
skill_route:
  capability: ""
  required: true | false
  candidate_providers: []
  selected_provider: "" | null
  selection_reason: ""
  dispatch_allowed: true | false
  fallback: core_protocol | user_materials | local_files | ask_user | stop
```

## Resolution Flow

```text
recipe.required_capabilities
  + platform available provider registry
  + task constraints
  + permission state
  -> ranked provider list
  -> selected_provider or fallback
```

## Ranking Rules

1. 安全性优先：只读、无登录、无私有写入优先。
2. 任务匹配优先：候选 skill 必须服务当前 capability。
3. 最小能力优先：静态资料优先简单读取，不直接上重型浏览器或下载工具。
4. 可回收性优先：输出能映射到 `sources[]`、`evidence[]`、`role-result` 的 skill 优先。
5. 已验证优先：本平台当前项目已验证过的 provider 优先。
6. 用户授权优先：登录、下载、写入私有库、社媒抓取必须有明确授权。

## Capability Provider Requirements

router 只声明每个 capability 需要什么样的 provider，不声明 provider 叫什么。

```yaml
source-acquisition:
  provider_requirements:
    - can_read_public_sources
    - can_return_text_or_structured_summary
    - can_attach_source_identity_when_available
    - can_respect_readonly_constraints
  fallback:
    - user_provided_materials
    - local_files
    - model_reasoning_with_boundaries

browser-automation:
  provider_requirements:
    - can_open_or_inspect_web_pages
    - can_preserve_readonly_mode
    - can_report_dynamic_content_boundaries
  fallback:
    - static_fetch
    - user_provided_screenshots
    - describe_unverified_dynamic_behavior

social-listening:
  provider_requirements:
    - can_process_public_or_user_provided_social_samples
    - can_preserve_platform_context
    - must_not_bypass_login_or_anti_abuse_controls
  fallback:
    - pasted_social_samples
    - exported_comments
    - no_social_claims

media-processing:
  provider_requirements:
    - can_process_user_provided_transcript_or_media_metadata
    - can_return_summary_or_segments
    - must_respect_download_and_rights_constraints
  fallback:
    - user_provided_transcript
    - user_provided_summary
    - metadata_only

knowledge-persistence:
  provider_requirements:
    - can_create_or_update_knowledge_artifact
    - can_report_write_target
    - must_require_permission_for_private_write
  fallback:
    - repository_markdown_artifact
    - inline_summary
    - no_private_write
```

## Recipe Overrides

recipe 可以缩小 provider 类型或排序 preference，但不能新增硬依赖，也不能要求某个具体 skill 必须存在。

示例：

```yaml
competitive-intelligence:
  source-acquisition:
    prefer:
      - provider_with_competitor_profile_schema
      - provider_with_public_web_sources
      - provider_with_market_signal_sources
  social-listening:
    prefer:
      - provider_with_user_feedback_samples
      - provider_with_social_context
```

如果某个平台刚好安装了某个竞品分析专用 skill，平台 adapter 可以把它注册成 `provider_with_competitor_profile_schema` 的一个实现。但这个名称不能写入主协议，也不能成为 think-tank 的默认依赖。

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
    candidate_providers:
      - provider_a
      - provider_b
    selected_provider: provider_a
    selection_reason: "provider_a 支持公开来源读取，并能回收到 sources[] 与 evidence[]"
    dispatch_allowed: true
    fallback: core_protocol

  - capability: social-listening
    required: false
    candidate_providers: []
    selected_provider: null
    selection_reason: "未获得登录/抓取授权，降级为用户提供样本"
    dispatch_allowed: false
    fallback: user_materials
```

## Anti-Patterns

- `竞品分析` 直接等于调用某个固定竞品分析 skill。
- 当前机器安装了某个社媒 skill 就默认抓取社媒内容。
- 当前机器安装了某个知识库 skill 就默认写用户私有库。
- 当前机器安装了某个媒体 skill 就默认下载视频。
- 在主协议或通用 router 中维护平台私有 skill 名单。
- route 失败时伪造 sources 或 evidence。

## Where Concrete Skill Names Belong

具体 skill 名只能出现在这些位置：

- `platforms/<platform>/`：平台 adapter 的示例映射或运行时发现说明。
- 本地、不上传的运行目录：例如当前项目的 `.codex/skills/`。
- 迁移审计文档：用于说明旧资产来源，不作为运行时依赖。
- 用户显式指定的任务上下文：例如用户要求使用某个已安装 skill。

具体 skill 名不应出现在：

- `protocol/` 的核心行为定义。
- `routing/skill-router.md` 的通用 provider selection 规则。
- 任何声称“只安装 think-tank 也可用”的最小安装路径中。
