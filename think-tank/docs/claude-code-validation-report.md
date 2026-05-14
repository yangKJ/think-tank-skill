# Claude Code Validation Report

本文记录 think-tank 在 Claude Code 平台的验证状态。

## 当前状态

```yaml
platform: claude-code
overall_status: in_progress
research_mode: verified_with_format_gap
council_mode: verified_as_single_agent_council_preflight
skill_entrypoint: verified_for_research_preflight
skill_discovery: verified
capability_auto_mapping: verified_partial_pre_invocation_decision
external_source_readonly: verified_partial
adapter_dispatch_attempt: adapter_dispatch_not_executed_verified_partial
dispatch_contract_validation: verified_partial_with_order_gap
dispatch_pre_invocation_decision: verified_partial
subagent_dispatch: planned
result_recovery: planned
external_skill_invocation: verified_partial_for_webfetch
minimal_runtime_contract: implemented_as_repeatable_contract
```

## 已完成验证

| 项目 | 文件 | 状态 |
|------|------|------|
| research mode preflight | `examples/claude-code-research-validation.md` | verified_with_format_gap |
| council mode preflight | `examples/claude-code-council-validation.md` | verified_as_single_agent_council_preflight |
| capability discovery | `examples/claude-code-capability-discovery.md` | skills_detected_mapping_mock |
| external source readonly | `examples/claude-code-external-source-readonly.md` | external_source_readonly_verified_partial |
| adapter dispatch attempt | `examples/claude-code-adapter-dispatch-attempt.md` | adapter_dispatch_not_executed_verified_partial |
| dispatch contract validation | `examples/claude-code-dispatch-contract-validation.md` | verified_partial_with_order_gap |
| dispatch pre-invocation decision | `examples/claude-code-dispatch-pre-invocation-validation.md` | verified_partial_pre_invocation_decision |

## Research Mode Preflight

测试任务：

```text
/think-tank research mode，研究一个跨平台 Skill 应如何在只有核心协议、没有外部工具时保持可用，并输出结论、依据、风险和行动建议。
```

验收判断：

```yaml
research_mode:
  status: verified_with_format_gap
  passed:
    - skill_entrypoint_triggered
    - protocol_files_used_as_source
    - conclusion_evidence_risk_action_boundary_output
    - no_external_tool_overclaim
  gaps:
    - selected_profiles_not_explicit
    - selected_capabilities_status_not_explicit
    - no_subagent_dispatch
```

## 不能声称

当前不能声称：

- Claude Code Agent Team 已验证。
- 真实 subagent 并行能力。
- `.claude/agents` 到 profiles 的映射已验证。
- `.claude/skills` 到 capabilities 的映射已验证。
- 完整 adapter 自动调度外部 skills 的能力。

## Council Mode Preflight

测试任务：

```text
使用 think-tank council mode，讨论：think-tank 是否应该内置 yt-dlp、obsidian、playwright-cli、xiaohongshu 等技能，还是只通过 capability 槽位调度它们？
```

验收判断：

```yaml
council_mode:
  status: verified_as_single_agent_council_preflight
  passed:
    - skill_loaded
    - selected_mode_declared
    - selected_profiles_declared
    - selected_capabilities_declared
    - capability_status_declared
    - execution_method_declared
    - disagreement_and_adjudication_present
    - no_external_skill_overclaim
  gaps:
    - true_subagent_dispatch_not_tested
    - external_skill_invocation_not_tested
    - result_recovery_not_tested
```

## 当前结论

Claude Code 已完成 think-tank 的 research/council preflight，完成了 browser/source acquisition 类 skills 的发现验证，并通过 WebFetch 完成了一次低风险外部只读 source acquisition 片段。

```yaml
claude_code_preflight:
  research_mode: verified_with_format_gap
  council_mode: verified_as_single_agent_council_preflight
  protocol_entrypoint: verified_for_preflight
  skill_discovery: verified
  capability_to_skill_mapping_reported: verified
  capability_auto_mapping: verified_partial_pre_invocation_decision
  external_source_readonly: verified_partial
  adapter_dispatch_attempt: verified_partial_direct_invocation
  dispatch_contract_validation: verified_partial_with_order_gap
  dispatch_pre_invocation_decision: verified_partial
  external_skill_invocation: verified_partial_for_webfetch
  result_recovery_contract: partial_manual_mapping
  true_multi_agent_runtime: planned
```

Claude Code 已经证明 `dispatch_decision` 可以在 WebFetch 调用前形成。当前不需要继续消耗 Claude Code 流量做同类验证。

仍未完成的是更高层级能力：

- 完整 adapter runtime
- 自动 result recovery contract
- fallback 链
- subagent runtime

这些不应继续通过 prompt 试探，而应进入实现或长期验证阶段。

## 后续计划

```yaml
next_phase: minimal_runtime_implementation
source: think-tank/platforms/claude-code/minimal-runtime.md
sample: think-tank/examples/claude-runtime-sample.json
failure_sample: think-tank/examples/claude-runtime-failure-sample.json
check: checks/claude_runtime_sample_check.py
```

目标输出样例见：

```text
think-tank/examples/claude-code-dispatch-contract-sample.md
```
