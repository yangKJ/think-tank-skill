# Claude Code Final Validation Prompt

本提示词用于最终低流量验证。只执行一次成功路径和一次失败路径，不重复做 preflight。

## 成功路径

```text
Skill(think-tank)

使用 think-tank research mode，按 Claude Code minimal runtime 执行 source-acquisition 成功路径验证。

要求：
1. 先读取：
   - think-tank/platforms/claude-code/minimal-runtime.md
   - think-tank/platforms/claude-code/dispatch-contract.md
   - think-tank/platforms/claude-code/skill-mapping.md
2. 目标 URL：https://httpbin.org/html
3. 在任何工具调用前输出 dispatch_request 和 dispatch_decision。
4. selected_skill 必须是 WebFetch。
5. 调用 WebFetch 读取目标 URL。
6. 输出 runtime_result，必须包含：
   - runtime: claude-code-minimal
   - mode: research
   - profile: source-collector
   - capability: source-acquisition
   - dispatch_request
   - dispatch_decision
   - invocation
   - recovery
   - sources[]
   - evidence[]
   - boundaries[]
   - quality_check
7. 不执行 fallback。
8. 不登录、不下载、不写 Obsidian、不抓社媒。
9. 不得声明 adapter_dispatch_runtime: verified。
10. 不得声明 result_recovery_contract: verified，除非能说明自动 recovery 机制。
```

## 失败路径

```text
Skill(think-tank)

使用 think-tank research mode，按 Claude Code minimal runtime 执行 source-acquisition 失败路径验证。

要求：
1. 目标 URL 使用一个不可访问目标，例如：https://invalid.example.invalid/
2. 在任何工具调用前输出 dispatch_request 和 dispatch_decision。
3. selected_skill 必须是 WebFetch。
4. 调用失败时，runtime_result 必须包含：
   - invocation.result_status: failed
   - recovery.result_recovered: false
   - sources: []
   - evidence: []
   - boundaries 中明确说明失败原因
   - boundaries 中明确说明 No fallback was executed
   - boundaries 中明确说明没有伪造 source 或 evidence
5. 不执行 fallback。
6. 不得把失败路径写成成功。
```

## 通过标准

```yaml
pass:
  - success_runtime_result_present
  - failure_runtime_result_present
  - dispatch_decision_before_invocation
  - success_sources_and_evidence_present
  - failure_sources_and_evidence_empty
  - fallback_not_claimed
  - no_full_adapter_overclaim
```
