# Codex Readiness Matrix

本文汇总 think-tank 在 Codex 主平台上的当前验收状态。

## 总结

```yaml
platform: codex
status: ready_before_claude_code_preflight
execution_model: single_agent_multi_profile_with_verified_partial_subagent_council
last_updated: 2026-05-15
```

Codex 当前已经足够作为 think-tank 的主工作平台继续使用。

它证明的是：

- 主协议可执行。
- 四个核心 mode 可执行。
- profiles 可以在 Codex 中分段模拟。
- capabilities 可以被选择、执行或降级。
- 本地资料和用户材料可以形成研究闭环。
- Markdown artifact 可以作为最小 knowledge-persistence 实现。
- 公开静态网页可以通过 Codex source-acquisition 只读回收。
- Browser localhost fixture 可以作为 optional browser-automation 验证。
- Codex subagents 可以执行只读 council 分析并回收 role_result，状态为 verified_partial。

它不证明：

- Claude Code Agent Team 可用。
- 真实多 agent 覆盖所有任务、外部 provider 和长期生命周期可用。
- Browser 外部网页 DOM 回收可用。
- Playwright CLI、yt-dlp、Obsidian、小红书等外部 skills 已集成。

## 验收矩阵

| 项目 | 状态 | 证据 |
|------|------|------|
| protocol structure | verified | `checks/protocol_check.py` |
| Codex validation package | verified | `checks/codex_validation_check.py` |
| schema samples | verified | `checks/schema_sample_check.py` |
| research mode | verified | `examples/codex-smoke-research.md` |
| council mode | verified | `examples/codex-council-validation.md` |
| review mode | verified | `examples/codex-review-validation.md` |
| strategy mode | verified | `examples/codex-strategy-validation.md` |
| minimal install | verified | `examples/codex-minimal-install-validation.md` |
| daily operational usage | verified | `examples/codex-operational-validation.md` |
| local source acquisition | verified | `examples/codex-local-source-validation.md` |
| Markdown artifact persistence | verified | `examples/codex-local-source-artifact.md` |
| external readonly source acquisition | verified | `examples/codex-external-source-validation.md` |
| browser localhost fixture | verified_optional | `examples/browser-automation-integration.md` |
| browser external readonly | blocked | `examples/codex-browser-external-blocked.md` |
| Codex true council subagents | verified_partial | `examples/codex-true-council-runtime.md` |
| Codex provider invocation matrix | established | `examples/codex-provider-invocation-matrix.json` |
| media-processing unavailable | verified_degradation | `examples/capability-degradation-media.md` |
| social-listening unavailable | verified_degradation | `examples/capability-degradation-social.md` |
| knowledge-persistence local fallback | verified | `examples/capability-degradation-knowledge.md` |
| Claude Code runtime | implemented_as_repeatable_contract | `platforms/claude-code/minimal-runtime.md` |
| Codex minimal runtime mirror | verified | `checks/minimal_runtime_execution_check.py` |

## Codex 验收命令

```bash
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/claude_code_validation_check.py
python3 checks/claude_dispatch_sample_check.py
python3 checks/claude_runtime_sample_check.py
python3 checks/minimal_runtime_execution_check.py
python3 checks/capability_queue_check.py
python3 checks/schema_sample_check.py
```

## 当前推荐工作流

```text
用户任务
  -> Codex operating-guide
  -> mode selection
  -> profile selection
  -> capability status check
  -> local/user/external readonly source acquisition
  -> multi-profile synthesis
  -> Markdown artifact when reusable
  -> quality checks
```

## 下一步停止点

Codex 侧做到以下状态即可停止，转入 Claude Code 平台验证：

```yaml
codex_ready_for_handoff:
  protocol: verified
  modes: verified
  local_sources: verified
  external_readonly_source: verified
  markdown_artifacts: verified
  degradation: verified
  browser_external_dom: blocked_with_reason
  claude_code_preflight_doc: ready
```

当前已经达到该状态。
