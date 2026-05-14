# Final Acceptance Plan

本文收敛 Phase 1 到 Phase 5 的最终验收安排。

## Phase Status

```yaml
phase_1_foundation_commit:
  status: done
  commit: 9d3e084
  excludes:
    - AGENTS.md
    - .DS_Store

phase_2_claude_code_minimal_runtime:
  status: implemented_as_repeatable_contract
  success_sample: examples/claude-runtime-sample.json
  failure_sample: examples/claude-runtime-failure-sample.json
  final_prompt: platforms/claude-code/final-validation-prompt.md

phase_3_codex_runtime_mirror:
  status: verified_with_local_fixture
  runner: platforms/codex/runtime/source_acquisition_minimal.py
  success_sample: examples/codex-runtime-sample.json
  failure_sample: examples/codex-runtime-failure-sample.json

phase_4_capability_queue:
  status: defined_and_checked
  roadmap: docs/capability-validation-roadmap.md

phase_5_claude_code_low_flow_validation:
  status: verified_partial_with_success_pre_invocation_and_failure_degradation
  prompt: platforms/claude-code/final-validation-prompt.md
  record: examples/claude-code-final-validation.md
  caveat: failure_path_pre_invocation_decision_not_confirmed_from_transcript
```

## 验收命令

```bash
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/claude_code_validation_check.py
python3 checks/claude_dispatch_sample_check.py
python3 checks/claude_runtime_sample_check.py
python3 checks/minimal_runtime_execution_check.py
python3 checks/capability_queue_check.py
python3 checks/schema_sample_check.py
python3 checks/runtime_contract_check.py
python3 checks/slot_contract_check.py
python3 checks/consensus_contract_check.py
python3 checks/research_protocol_check.py
```

## 不能声称

- 不能声称 Claude Code 完整 adapter runtime 已验证。
- 不能声称自动 result recovery contract 已验证。
- 不能声称 Browser 外部 DOM 回收已验证。
- 不能声称 Obsidian、yt-dlp、whisper、小红书等外部能力已集成。
