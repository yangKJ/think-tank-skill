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
  success_sample: examples/runtime/claude-runtime-sample.json
  failure_sample: examples/runtime/claude-runtime-failure-sample.json
  final_prompt: platforms/claude-code/final-validation-prompt.md

phase_3_codex_runtime_mirror:
  status: verified_with_local_fixture
  runner: platforms/codex/runtime/source_acquisition_minimal.py
  success_sample: examples/runtime/codex-runtime-sample.json
  failure_sample: examples/runtime/codex-runtime-failure-sample.json

phase_4_capability_queue:
  status: defined_and_checked
  roadmap: docs/capability-validation-roadmap.md

phase_5_claude_code_low_flow_validation:
  status: verified_partial_with_success_pre_invocation_and_failure_degradation
  prompt: platforms/claude-code/final-validation-prompt.md
  record: think-tank/examples/platforms/claude-code/claude-code-final-validation.md
  caveat: failure_path_pre_invocation_decision_not_confirmed_from_transcript

legacy_think_tank_full_migration:
  status: complete
  migration_record: docs/legacy-think-tank-full-migration.md
  safety_runtime: runtime/safety.py
  templates: templates/
  claude_legacy_runtime: platforms/claude-code/legacy-team-runtime.md

v0_3_research_agent_full_migration:
  status: complete
  inventory: docs/research-agent-full-inventory.md
  interop: docs/external-skill-interoperability.md
  private_domain_knowledge_in_core: false
  check: checks/research_agent_full_migration_check.py

v0_4_agent_council_full_migration:
  status: complete
  inventory: docs/agent-council-full-inventory.md
  runtime_migration: docs/agent-council-runtime-migration.md
  history_index: docs/agent-council-history-index.md
  runtime_helper: runtime/council.py
  check: checks/agent_council_full_migration_check.py

v0_5_specialist_subagent_runtime:
  status: implemented_contract_and_runtime_primitives
  contract: protocol/subagent-runtime-contract.md
  runtime_helper: runtime/subagent.py
  schema: schemas/role-result.schema.json
  prompt_pack: profiles/prompt-pack.md
  caveat: true_parallel_runtime_not_verified
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
python3 checks/runtime_planner_check.py
python3 checks/slot_resolver_check.py
python3 checks/state_model_check.py
python3 checks/consensus_runtime_check.py
python3 checks/runtime_result_schema_check.py
python3 checks/codex_runtime_pipeline_check.py
python3 checks/claude_runtime_pipeline_spec_check.py
python3 checks/runtime_e2e_fixture_check.py
python3 checks/runtime_safety_check.py
python3 checks/template_check.py
python3 checks/legacy_think_tank_migration_check.py
python3 checks/research_agent_full_migration_check.py
python3 checks/agent_council_full_migration_check.py
python3 checks/council_runtime_check.py
python3 checks/subagent_runtime_check.py
python3 checks/role_result_schema_check.py
python3 checks/specialist_runtime_contract_check.py
```

## 不能声称

- 不能声称 Claude Code 完整 adapter runtime 已验证。
- 不能声称自动 result recovery contract 已验证。
- 不能声称 Browser 外部 DOM 回收已验证。
- 不能声称 Obsidian、yt-dlp、whisper、小红书等外部能力已集成。
