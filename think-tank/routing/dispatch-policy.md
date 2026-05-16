# Dispatch Policy

本文定义 think-tank 什么时候可以调用 optional peer skill，什么时候必须降级。

## Dispatch States

```yaml
dispatch_state:
  planned: "已选择候选，但尚未调用"
  skipped: "因不需要、不可用或未授权而跳过"
  invoked: "已真实调用"
  failed: "调用失败"
  recovered: "调用结果已回收到 think-tank 输出结构"
```

## Required Pre-Dispatch Fields

调用任何 peer skill 前，必须形成：

```yaml
dispatch_request:
  intent: ""
  recipe: ""
  mode: ""
  capability: ""
  task: ""
  target: ""
  constraints: []
  evidence_policy: ""

dispatch_decision:
  candidate_peer_skills: []
  selected_peer_skill: ""
  selection_reason: ""
  invocation_method: ""
  fallback: ""
  risk_level: low | medium | high
  dispatch_allowed: true | false
```

## Allow Rules

允许自动调用 peer skill 的常见条件：

- 只读。
- 目标是本地文件、用户提供材料或公开静态资料。
- 不需要登录。
- 不需要写用户私有库。
- 不会下载大文件或受版权限制内容。
- 输出可被结构化回收。

## Require Explicit Permission

以下操作需要用户明确授权：

- 登录态访问。
- 社媒抓取、评论抓取、互动行为。
- 写入 Obsidian、NotebookLM 或其他私有知识库。
- 下载视频、音频或大文件。
- 发布、评论、点赞、收藏、删除等外部可见行为。
- 长时间后台监控或自动化任务。

## External Provider And CLI Invocation Contract

当 optional peer skill 需要转接外部 provider、第三方 CLI、登录态工具或付费额度时，必须先生成可审查的调用契约，而不是直接执行。

```yaml
external_provider_invocation_contract:
  provider:
  provider_family:
  command_or_endpoint:
  default_mode: dry_run | preview_only | manifest_only
  execute_flag_required: true
  confirmation_required:
    - provider
    - input_content
    - provider_safe_input
    - quota_or_cost
    - output_directory
    - overwrite_policy
  secrets_policy:
    read_from_env_or_local_config_only: true
    stored_in_artifact: false
    printed_to_logs: false
  artifact_policy:
    command_preview_allowed: true
    sanitized_response_required: true
    api_keys_stored_in_artifact: false
  selection_is_invocation: false
  provider_invoked: false
```

默认模式必须是 `dry_run`、`preview_only` 或 `manifest_only`。真实执行必须有显式执行开关，例如 `--execute`，并且必须额外确认成本、额度、输出路径和覆盖策略。

如果 provider CLI 生态存在多种命令形态，主流程只能依赖统一队列或 adapter payload，不能把未经实测的命令名写成事实。命令模板中的变量必须显式列出，禁止把 `.env`、cookie、token、账号状态或绝对私有路径注入 prompt、queue 或命令行。

## Degrade Rules

如果 peer skill 缺失、不可用、失败或未授权：

```yaml
degrade_to:
  - core_protocol
  - user_provided_materials
  - local_files
  - partial_output
  - ask_user_if_blocking
```

降级不是失败。失败的是把降级结果说成完整验证。

## Status Claims

```yaml
installed: "skill 文件存在"
selected: "本次路由选择为候选"
invoked: "本次真实调用"
recovered: "结果已映射回 think-tank 结构"
verified: "真实调用成功且有可检查产物"
```

禁止：

- installed -> verified
- selected -> invoked
- invoked -> recovered
- recovered -> full runtime verified

每一层都必须有证据。
