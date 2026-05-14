# Codex Provider Registry

本文定义 Codex 平台如何把项目本地 `.codex/skills/` 中的同级技能提供给 think-tank 使用。

这不是 think-tank 主协议的一部分，也不是所有用户必须拥有的技能清单。它只是 Codex adapter 的本地能力发现机制。

## Position

```yaml
layer: platforms/codex
purpose: discover_local_peer_skills_as_capability_providers
owns_protocol: false
owns_skills: false
required_for_core_think_tank: false
missing_registry_behavior: degrade_to_core_protocol
```

## Correct Flow

```text
.codex/skills/
  -> platforms/codex/runtime/provider_registry.py
  -> available_providers[]
  -> routing/skill-router.md
  -> routing/dispatch-policy.md
  -> platform invocation
  -> routing/result-recovery.md
```

`provider_registry.py` 只做发现和描述，不执行 skill。

## Provider Descriptor

每个被发现的同级 skill 会被转换成 provider descriptor：

```yaml
provider:
  id: ""
  source: ".codex/skills/<name>/SKILL.md"
  platform: codex
  provider_type: local_peer_skill
  capabilities: []
  access_level: readonly | write | network | private | privileged
  requires_permission: true | false
  recovery_targets: []
  status: available
  verification: unknown
```

## Selection Boundary

发现 provider 不等于调用 provider。

```yaml
installed: true
available_provider: true
selected_by_router: not_yet
invoked: false
verified: false
```

只有某次任务实际完成以下链路，才能声明该 provider 的本次能力为 verified：

```text
skill_route
  -> dispatch_decision
  -> invocation
  -> result_recovery
  -> sources/evidence/artifact/boundaries
```

## Missing Skills

如果用户只安装 think-tank，没有任何其他 `.codex/skills/`：

```yaml
available_providers: []
fallback: core_protocol
allowed_output: conclusion_with_boundaries
forbidden_output: claim_external_skill_verified
```

这正是 think-tank 的最小可用路径。

## Where Concrete Names Live

具体 skill 名称只允许出现在 Codex adapter 层：

- `platforms/codex/provider-registry.md`
- `platforms/codex/runtime/provider_registry.py`
- `platforms/codex/trigger-routing.md`
- 本地 `.codex/skills/`
- 安装或迁移审计文档

它们不应进入：

- `protocol/`
- `routing/skill-router.md`
- 跨平台 mode 定义

## Usage

检查当前项目本地可用 provider：

```bash
python3 think-tank/platforms/codex/runtime/provider_registry.py
```

输出可传给 `routing/skill-router.md` 的 `available_providers` 输入。
