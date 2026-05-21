# Stable Readiness Matrix

本文记录 `think-tank` 距离 stable release 还差什么。

## 当前状态

```yaml
release_posture: stable_release
stable_release_ready: true
last_evaluated_by_repo_gate: true
```

## Matrix

| area | stable requirement | current status | result |
|------|--------------------|----------------|--------|
| public release posture | `stable_candidate_or_stronger` | `stable_release` | pass |
| protocol core | pass | pass | pass |
| codex foundation | pass | pass | pass |
| runtime provenance | pass | pass | pass |
| privacy boundary | pass | pass | pass |
| package boundary | pass | pass | pass |
| provider invocation evidence | at least 3 real provider invocations with recovery | 3 public proofs recorded | pass |
| browser external readonly | `verified_partial_or_verified` | `verified_partial` | pass |
| multi-agent beyond readonly council | `verified_partial_or_verified` | `verified_partial` | pass |
| long-running subagent lifecycle | not `not_verified` | `verified_partial` | pass |
| clean environment repeatability | documented + CI | pass | pass |

## Current Interpretation

- 仓库已经达到稳定产品级 1.0 的最小公开工程标准
- stable release 的 runtime 证据 blocker 已清空
- 当前 stable 姿态建立在显式边界之上，而不是宣称所有 optional provider 都默认可用

## Required Next Evidence

1. 扩展 subagent 内部 external provider 覆盖
2. 扩展跨平台 adapter parity
3. 把更多 clean-environment reruns 纳入公开样例
