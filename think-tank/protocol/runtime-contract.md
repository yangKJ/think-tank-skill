# Runtime Contract

本文定义 think-tank v0.2 的平台无关 runtime contract。

它吸收旧 research think-tank `workflow.py` 的工程经验，但不继承旧 Claude Code Team 实现。

## 目的

runtime contract 解决一个问题：

> think-tank 如何从用户请求进入可审计、可降级、可回收的执行流程。

## Runtime Pipeline

```text
intake
  -> trigger_resolution
  -> mode_selection
  -> runtime_plan
  -> capability_slot_resolution
  -> stage_execution
  -> result_recovery
  -> synthesis
  -> quality_check
```

## Trigger Resolution

```yaml
trigger_resolution:
  input: user_request
  output:
    selected_mode: research | council | review | strategy
    selected_runtime_profile: quick | standard | deep
    strict: true | false
    fallback_behavior: no_match_degrade | use_default_mode | ask_for_clarification
```

`selected_runtime_profile` must follow `protocol/runtime-profile-contract.md`.
Do not treat `deep` as the default. Pick the lightest profile that can still
produce a useful, honest result.

规则：

- `strict: true` 时，无匹配不得自动使用 full/default workflow。
- `strict: false` 时，可以使用默认 mode，但必须说明 fallback。
- trigger 只决定执行入口，不得绕过 mode selection。

## Runtime Plan

```yaml
runtime_plan:
  mode: ""
  priority: high | medium | low
  complexity: low | medium | high
  stages:
    - name: collection
      max_rounds: 1
      timeout: optional
      load_mode: minimal | standard | comprehensive
      required_capabilities: []
      optional_capabilities: []
```

## Stage Config

每个阶段必须声明：

- `name`
- `required_capabilities`
- `optional_capabilities`
- `max_rounds`
- `timeout` 或 stop condition
- `expected_output`
- `failure_behavior`

## Failure Behavior

```yaml
missing_required_capability:
  action: degrade_or_stop
  output_required:
    - missing_capability
    - attempted_mapping
    - boundary

missing_optional_capability:
  action: continue_with_boundary
  output_required:
    - omitted_capability
    - consequence

stage_timeout:
  action: synthesize_partial
  output_required:
    - completed_stage_results
    - missing_stage_results
    - confidence_impact
```

## Platform Boundary

平台 adapter 可以实现：

- 文件状态
- subagent 派发
- tool invocation
- browser automation
- memory/artifact write
- team cleanup with zombie detection

平台 adapter 不得改变：

- mode 语义
- stage 顺序
- capability 状态语义
- output contract
- quality gates

## Shutdown Handling

Claude Code 等平台存在已知 shutdown 死锁 bug。平台 adapter 必须：

1. 实现超时保护机制（见 `protocol/shutdown-contract.md`）
2. 检测 zombie team（`config.json` 中 `tmuxPaneId: "in-process"`）
3. 在输出中包含手动清理提示
4. 不得假设 `TeamDelete` 一定成功

参考：
- `protocol/shutdown-contract.md` - Shutdown 流程
- `protocol/session-gc-contract.md` - Zombie team 清理
- `protocol/filesystem-message-bus.md` - Teamless 协作（事前规避）

## Verification Status

```yaml
runtime_contract_v0_2: specified
reference_source: old_research_think_tank_workflow_engine
implementation_status:
  codex: minimal_runtime_mirror_verified_with_local_fixture
  claude_code: verified_partial_with_success_pre_invocation_and_failure_degradation
not_verified:
  - full_adapter_runtime
  - automatic_result_recovery
  - subagent_parallel_runtime
related_contracts:
  - protocol/shutdown-contract.md (shutdown handling)
  - protocol/state-result-contract.md (team cleanup)
  - protocol/session-gc-contract.md (zombie gc)
  - protocol/filesystem-message-bus.md (teamless mode)
```
