# Open Source Release

本文定义 `think-tank` 当前作为公开仓库发布时的承诺边界。

## 当前结论

```yaml
release_posture: public_beta
safe_to_publish: true
safe_to_market_as_stable_product: false
current_default_release: full_repo_public_beta
default_public_claim:
  - protocol-first high-level Skill
  - Codex-first verified foundation
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
versioning_hint: 0.x
audience: early_adopters
support_message: protocol_and_codex_foundation_are_ready
warning_message: optional providers and broader runtime remain evidence-based beta
```

README、介绍页、示例仓库和演示材料都应保持同样的边界表述。

## 发行档

仓库当前维护两个发行档定义：

- `full_repo_public_beta`
- `skill_core_only_bundle`

当前默认公开发行档是 `full_repo_public_beta`。That means the current default public release keeps `leader-runtime/` in the repository as a sibling runtime layer, not as think-tank core.

对应机器可检查清单见：

```text
open-source-packages.yaml
```

## 发布门禁

以下检查应全部通过：

```bash
python3 checks/open_source_release_suite.py
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/schema_sample_check.py
python3 checks/minimal_runtime_execution_check.py
python3 checks/release_privacy_check.py
python3 checks/open_source_release_check.py
```

## 需要持续补强的点

1. provider invocation evidence
2. external browser runtime evidence
3. long-running subagent lifecycle evidence
4. public onboarding and example freshness
5. semantic consistency checks beyond file presence

## 升级到更强公开承诺前的条件

只有当以下条件成立，才考虑把 `public_beta` 提升为更强承诺：

- 至少 3 个 optional providers 形成真实 invocation + recovery 样例
- readonly council 之外的多 agent runtime 有独立证据
- 外部用户 quickstart 可以在干净环境重复通过
- release gate 能检查文案、边界和隐私问题
