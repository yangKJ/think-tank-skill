# Stable Release Criteria

本文定义 `think-tank` 何时可以从 `public_beta` 升级为更强公开承诺。

## 目标

`stable` 在本仓库中的含义不是“所有能力都存在”，而是：

- 公开承诺和真实证据一致
- 核心路径在干净环境可重复通过
- optional providers 至少有有限但真实的端到端证据
- 多 agent runtime 不再只停留在只读局部样例

## 必须满足

```yaml
stable_release_requirements:
  public_release_posture:
    required: stable_candidate_or_stronger
  core_contract:
    protocol_check: pass
    codex_validation_check: pass
    schema_sample_check: pass
    minimal_runtime_execution_check: pass
    runtime_provenance_check: pass
  privacy_and_boundary:
    release_privacy_check: pass
    public_package_boundary_check: pass
    open_source_release_check: pass
  provider_evidence:
    min_verified_or_verified_partial_invoked_providers: 3
    requires_dispatch_decision: true
    requires_invocation_log: true
    requires_result_recovery: true
  browser_evidence:
    external_browser_readonly: verified_partial_or_verified
  multi_agent_evidence:
    beyond_readonly_council: verified_partial_or_verified
    long_running_lifecycle: not_not_verified
  clean_environment_repeatability:
    documented_quickstart: true
    ci_release_gate: pass
    no_repo_local_path_leaks: true
```

## 不足以构成 stable 的情况

- 只有本地协议检查通过
- 只有 `installed` 或 `selected`，没有真实 provider invocation
- 只有 localhost browser fixture
- 只有 readonly council subagent 样例
- 只有单 agent 多 profile 模拟
- 只有文档承诺，没有可检查样例

## 建议升级顺序

```text
public_beta
  -> repeatable_public_beta
  -> stable_candidate
  -> stable_release
```

## 当前已知关键缺口

1. 外部 provider 的真实 invocation 证据数量不足
2. browser external readonly 仍未达到 `verified_partial_or_verified`
3. 多 agent runtime 仍主要停留在 readonly council `verified_partial`
4. 长生命周期 subagent 仍未形成稳定证据
