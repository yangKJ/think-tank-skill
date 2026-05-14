# Routing Policy Schema

本文定义 think-tank routing policy 的平台无关配置结构。

routing policy 用来把用户或项目的自然语言习惯、任务偏好和 provider 选择规则配置化。它替代在 think-tank core 中硬编码触发词或具体 skill 名。

## Position

```yaml
layer: routing
purpose: configure_triggers_intents_recipes_capabilities_and_provider_preferences
owns_protocol: false
owns_platform_runtime: false
required_for_core_think_tank: false
missing_policy_behavior: use_adapter_defaults_or_core_protocol
```

think-tank core 只定义：

- intent 类型
- mode 类型
- recipe 语义
- capability slots
- 输出结构
- 质量门禁

policy 定义：

- 哪些触发词或正则匹配到哪个 intent
- 使用哪个 recipe 和 mode
- 本项目偏好哪些 providers
- 禁用哪些 providers
- 失败时如何降级

## Precedence

```text
user_explicit_instruction
  > project_local_policy
  > user_global_policy
  > platform_default_policy
  > provider_registry
  > core_protocol_fallback
```

用户本次明确指令永远最高。例如用户说“只用小红书样本，不要用网页搜索”，即使 policy 允许网页 provider，本次也必须拒绝网页 provider。

## Policy Shape

```yaml
version: 1

metadata:
  name: ""
  description: ""

defaults:
  fallback: core_protocol
  missing_provider_behavior: degrade_to_core_protocol
  require_permission_for:
    - private_write
    - social_scraping
    - media_download

routes:
  - id: ""
    priority: 100
    enabled: true
    triggers:
      patterns: []
      match: regex | contains | exact
    intent: ""
    mode: ""
    recipe: ""
    profiles: []
    capabilities: []
    providers:
      prefer: []
      allow: []
      deny: []
    fallback: core_protocol | user_materials | local_files | ask_user | stop
```

## Provider Rules

`providers.prefer`、`providers.allow`、`providers.deny` 可以使用两类值：

1. provider id：由平台 provider registry 发现的具体同级 skill 或工具。
2. provider tag：平台 registry 或 policy 约定的抽象标签。

通用 policy 可以使用 provider tag；项目本地 policy 可以使用具体 provider id。

示例：

```yaml
providers:
  prefer:
    - provider_with_social_context
  allow:
    - xiaohongshu
  deny:
    - generic_web_search
```

## Route Matching

多个 route 命中时：

1. `enabled: false` 的 route 跳过。
2. `priority` 数值更高者优先。
3. 用户显式指定 intent、mode、recipe 或 provider 时覆盖 route 默认值。
4. 同优先级时按配置文件顺序。
5. 无 route 命中时进入 adapter 默认策略或 core protocol fallback。

## Safety Rules

- policy 可以允许 provider，但不能绕过 `dispatch-policy.md`。
- policy 可以偏好社媒或下载 provider，但不能自动授予登录、抓取、下载或私有写入权限。
- policy 命中不等于 provider 已执行。
- provider 被选择不等于结果已验证。
- route 失败时必须保留 boundaries，不能伪造 sources 或 evidence。

## Minimal Install

只安装 think-tank、没有任何 policy 和外部 provider 时：

```yaml
policy_status: missing
available_providers: []
fallback: core_protocol
allowed: true
```

这保证 think-tank 作为高阶 Skill 的最小可用性。
