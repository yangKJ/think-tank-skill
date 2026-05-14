# Subagent Runtime Contract

本文定义 think-tank v0.5 的专业 subagent runtime 契约。

## 目的

think-tank 可以在两个执行层级运行：

```yaml
specialist_subagent_runtime:
  authority: higher
  condition: platform can run independent specialist contexts

single_agent_multi_profile_fallback:
  authority: lower
  condition: platform lacks verified subagent runtime
```

单 agent 多 profile 是可用降级，不是最终权威形态。专业 subagent runtime 的目标是让不同 profile 拥有独立上下文、独立输入、独立输出和可回收结果。

## Dispatch Contract

```yaml
subagent_task:
  task_id: string
  profile: string
  mode: research | council | review | strategy
  objective: string
  input_context: []
  required_capabilities: []
  expected_output_schema: role-result
  independence_boundary: string
```

## Role Result Contract

每个专业 subagent 必须返回：

```yaml
role_result:
  profile: string
  execution_method: specialist_subagent | single_agent_multi_profile_fallback | external_platform_adapter
  claim: string
  evidence: []
  sources: []
  risks: []
  objections: []
  recommendations: []
  confidence: low | medium | high
  boundaries: []
  status: completed | partial | failed | blocked
```

## Recovery Rule

主 runtime 只能汇总真实返回的 `role_result`。

禁止：

- 子 agent 没返回结果时伪造观点。
- fallback 路径声称 specialist runtime。
- 把同一上下文里的角色扮演说成独立 subagent。
- 把工具安装状态说成 profile 执行成功。

## Quality Gate

最终输出必须标注：

```yaml
execution_method: specialist_subagent | single_agent_multi_profile_fallback | mixed
specialist_independence: verified | partial | unavailable
authority_level: specialist_independent | lower_fallback_single_context
```

## 状态

```yaml
subagent_runtime_contract: specified
codex_specialist_runtime: adapter_specified
claude_code_specialist_runtime: adapter_specified
true_parallel_runtime_verified: false
fallback_runtime_supported: true
```
