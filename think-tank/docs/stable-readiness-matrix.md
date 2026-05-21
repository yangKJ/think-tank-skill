# Stable Readiness Matrix

本文记录 `think-tank` 距离 stable release 还差什么。

## 当前状态

```yaml
release_posture: public_beta
stable_release_ready: false
last_evaluated_by_repo_gate: true
```

## Matrix

| area | stable requirement | current status | result |
|------|--------------------|----------------|--------|
| public release posture | `stable_candidate_or_stronger` | `public_beta` | blocked |
| protocol core | pass | pass | pass |
| codex foundation | pass | pass | pass |
| runtime provenance | pass | pass | pass |
| privacy boundary | pass | pass | pass |
| package boundary | pass | pass | pass |
| provider invocation evidence | at least 3 real provider invocations with recovery | 3 public proofs recorded | pass |
| browser external readonly | `verified_partial_or_verified` | `verified_partial` | pass |
| multi-agent beyond readonly council | `verified_partial_or_verified` | `not_verified` | blocked |
| long-running subagent lifecycle | not `not_verified` | `not_verified` | blocked |
| clean environment repeatability | documented + CI | pass | pass |

## Current Interpretation

- 仓库已经达到稳定公开 beta 的工程标准
- 仓库还没有达到 stable release 的证据标准
- 当前 blocker 主要不是文档或 gate，而是真实能力证据

## Required Next Evidence

1. 至少一条超出 readonly council 的多 agent runtime 样例
2. 至少一条 long-running lifecycle 证据
3. 公开发布姿态从 `public_beta` 升级到 `stable_candidate_or_stronger`
