# Codex True Council Runtime Validation

本文记录 Codex 平台对 think-tank council mode 的真实 subagent 派发验证。

## Test Task

```text
开会讨论：think-tank 是否应该把真实 subagent runtime 放在 platform adapter，而不是 core？
```

## Runtime Result

```yaml
platform: codex
mode: council
runtime: codex_parallel_subagent_runtime
status: verified_partial
executed_at: 2026-05-15
main_agent_role: facilitator_synthesizer
subagents_spawned: true
subagent_count: 3
profiles:
  - architect
  - skeptic
  - product-strategist
role_results_recovered: true
execution_method: codex_spawn_agent_parallel_explorers
authority_level: specialist_independent_for_repo_readonly_analysis
```

## Role Results

### architect

```yaml
profile: architect
position: >
  真实 subagent runtime 应放在 platform adapter，而不是 core。
  core 应保留平台无关协议、任务/结果契约、schema、fallback 标签和聚合原语。
evidence:
  - protocol/runtime-contract.md 将 subagent 派发列为 platform adapter 可实现项。
  - platforms/README.md 允许 runtime 和 subagent 调用方式按平台不同。
  - runtime/README.md 明确 subagent.py 不创建真实外部 agent。
risks:
  - runtime 下沉到 core 会污染协议边界。
  - adapter 若缺少统一契约检查会出现平台漂移。
recommendations:
  - core 保持 protocol、schema、fallback 和 aggregation primitives。
  - dispatch、生命周期、工具权限和 result recovery 放到 platforms/<platform>/。
confidence: high
boundaries:
  - 只验证 Codex subagent 派发和只读 repo 分析，不验证外部工具调用。
```

### skeptic

```yaml
profile: skeptic
position: >
  支持真实 subagent runtime 放在 adapter，但当前只能证明 Codex 独立 subagent 分析
  和结果回收已发生，不能证明所有平台或所有外部 provider runtime 已完成。
evidence:
  - protocol/subagent-runtime-contract.md 要求 fallback 不得冒充 specialist runtime。
  - platforms/codex/specialist-subagent-runtime.md 原状态为 true_parallel_subagent_runtime: not_verified。
  - runtime/subagent.py 只提供 SubagentTask、RoleResult 和 aggregation helper。
risks:
  - runtime_helper: verified 容易被误读为真实平台 runtime verified。
  - fallback 若不标注 authority_level，会继续被误报为多 agent。
recommendations:
  - 平台必须提供独立 task payload、调用记录、role_result 回收和失败样本。
  - 只要角色结果来自 fallback，就不得声明 specialist_independence: verified。
confidence: medium
boundaries:
  - 本次未执行 Claude Code Team、外部 worker 或外部 provider 调用。
```

### product-strategist

```yaml
profile: product-strategist
position: >
  产品路线应坚持 core 定义正确的 think-tank，adapter 负责具体平台怎么真实跑起来。
evidence:
  - runtime-contract.md 保留 mode/stage/output/quality gates 在协议层。
  - platforms/README.md 允许平台差异包括 runtime、hook、权限和记忆落点。
  - docs/v0.5-specialist-subagent-runtime.md 明确不声称所有平台真实并发已完成。
risks:
  - core 承担真实派发会削弱跨平台复用价值。
  - adapter 能力未验证却统一宣称会损害发布可信度。
recommendations:
  - 产品文案使用分层承诺：core contract verified，Codex subagent verified_partial。
  - 下一阶段优先补 adapter acceptance tests，而不是扩 core。
confidence: high
boundaries:
  - 本结论是 Codex 平台验证结果，不适用于 Claude Code 的完成声明。
```

## Synthesis

```yaml
consensus:
  - 真实 subagent runtime 应属于 platform adapter。
  - core 保持协议、schema、profile/capability 语义、fallback 和聚合原语。
  - Codex 已验证独立 subagent 只读分析和 role_result 回收。
disagreements:
  - skeptic 要求继续收紧 runtime_helper 的措辞，避免被误读为 full runtime。
risks:
  - 不得把 Codex verified_partial 扩写成所有平台 verified。
  - 不得把外部 provider discovery 扩写成外部 skill invocation verified。
action_items:
  - 更新 Codex specialist runtime 状态为 verified_partial。
  - 建立 provider invocation matrix。
  - 增加检查脚本防止无 capability 的 route 误选 provider。
final_recommendation: >
  Codex 平台可声明 true multi-agent council 的只读分析路径 verified_partial；
  full platform adapter runtime、外部 provider 调用和 Claude Code Team runtime 继续按平台验证。
```

## Boundaries

- 本次使用 Codex subagents 做只读仓库分析，没有修改文件。
- 本次验证的是独立 profile context、独立 role_result 和主 agent 汇总。
- 本次不验证外部工具调用、长期状态、文件写入、Claude Code Team 或所有 provider 自动调用。

