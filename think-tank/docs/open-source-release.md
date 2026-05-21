# Open Source Release

本文定义 `think-tank` 当前作为公开仓库发布时的承诺边界。

## 当前结论

```yaml
release_posture: stable_release
safe_to_publish: true
safe_to_market_as_stable_product: true
current_default_release: skill_core_only_bundle
default_public_claim:
  - protocol-first high-level Skill
  - Codex-first verified foundation
  - stable release with explicit capability boundaries
  - explicit capability evidence states
  - optional providers require per-provider validation
```

## 可以公开承诺的内容

- `think-tank` 是跨平台、可复用的高阶 Skill core
- 协议、mode、profiles、capabilities、routing 和 runtime provenance 已经形成可检查结构
- Codex 主路径可用于日常 research、review、strategy 和受控 council 任务
- capability 缺失时可以降级，而不是伪造成功
- 仓库用 `verified`、`verified_partial`、`planned`、`blocked` 区分能力状态

## 不能公开承诺的内容

- 所有外部 provider 默认可用
- 所有平台都已有完整 runtime
- 真实多 agent 已覆盖任意任务
- 安装同级 skill 就等于已经端到端打通
- 浏览器、社媒、下载、私有知识库写入已成为默认能力

## 发布建议

对外推荐姿态：

```yaml
versioning_hint: 1.0
audience: production-minded teams that accept explicit provider boundaries
support_message: protocol_and_codex_foundation_are_stably_releasable
warning_message: optional providers and broader cross-platform runtime remain evidence-based and scoped
```

README、介绍页、示例仓库和演示材料都应保持同样的边界表述。

## 发行档

仓库当前只维护一个默认公开发行档定义：

- `skill_core_only_bundle`

当前默认公开发行档是 `skill_core_only_bundle`。In other words, the current default public release is `skill_core_only_bundle`。`leader-runtime` 应作为独立 sibling 项目存在，而不是继续留在当前 Skill 仓库里。

对应机器可检查清单见：

```text
public-release-manifest.yaml
```

## 发布门禁

默认公开发布只要求 release gate 通过：

```bash
python3 checks/open_source_release_suite.py
```

展开后包含：

```bash
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/schema_sample_check.py
python3 checks/minimal_runtime_execution_check.py
python3 checks/release_privacy_check.py
python3 checks/open_source_release_check.py
```

检查分层见：

```text
think-tank/docs/validation-tiers.md
```

不要把 local provider validation 当成默认开源承诺。

## 需要持续补强的点

1. broader external provider coverage inside subagents
2. cross-platform adapter parity beyond Codex
3. public onboarding and example freshness
4. semantic consistency checks beyond file presence

## 升级到更强公开承诺前的条件

当前仓库已经满足 stable release 所需的最小公开条件；后续继续补强的是覆盖面，而不是是否允许公开声明为 stable。

仍需持续维护的条件：

- 至少 3 个 optional providers 形成真实 invocation + recovery 样例
- external browser readonly 至少达到 `verified_partial`
- readonly council 之外的多 agent runtime 有独立证据
- 外部用户 quickstart 可以在干净环境重复通过
- release gate 能检查文案、边界和隐私问题
