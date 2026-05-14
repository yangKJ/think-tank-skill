# Claude Code Dispatch Contract

本文定义 Claude Code adapter 的最小 dispatch 契约。

该契约只属于 Claude Code 平台适配层，不改变 think-tank 主协议。它的目标是把协议层选出的 capability 映射到当前 Claude Code 环境可用的 skill/tool，并把结果回收到 think-tank 输出结构。

## 当前定位

```yaml
platform: claude-code
contract_version: 0.1.0
status: design_ready
verified_runtime: false
```

当前已验证：

- think-tank skill entrypoint 可以加载。
- research/council preflight 可以执行。
- browser/source acquisition 类 skills 可以被发现。
- WebFetch 可以直接读取公开静态网页。

当前未验证：

- adapter 自动 dispatch。
- fallback。
- result recovery contract。
- subagent 并发。

## Dispatch 输入

最小输入：

```yaml
dispatch_request:
  mode: research
  profile: source-collector
  capability: source-acquisition
  task: ""
  target: ""
  constraints:
    - readonly
    - no_login
    - no_download
    - no_private_write
  evidence_policy:
    network: allowed | disallowed | required
    citations: optional | required
```

## Dispatch 决策

Claude Code adapter 必须显式输出：

```yaml
dispatch_decision:
  selected_capability: ""
  candidate_skills: []
  selected_skill: ""
  selection_reason: ""
  invocation_method: ""
  fallback_skills: []
  risk_level: low | medium | high
  status: planned | dispatched | degraded | blocked
```

选择顺序：

1. 读取 `platforms/claude-code/skill-mapping.md`。
2. 找出 capability 对应的候选 skills。
3. 过滤高风险或不符合约束的 skill。
4. 优先选择只读、无需登录、可回收文本结果的 skill。
5. 如果没有可用 skill，输出 `status: degraded` 或 `status: blocked`。
6. 如果调用 skill，记录 `invocation_method`。

## Source Acquisition 最小映射

`source-acquisition` 的低风险候选：

```yaml
source_acquisition:
  preferred:
    - web-access
    - WebFetch
  fallback:
    - google-ai-mode-skill
    - mcp-cli
    - juejin-search
    - 36kr-hotlist
  blocked_by_default:
    - social-listening skills
    - media-processing skills
    - private knowledge base write skills
```

对于公开静态网页，最小 dispatch 应选择：

```yaml
selected_skill: web-access
invocation_method: WebFetch
risk_level: low
```

## Dispatch 日志

每次 dispatch 必须输出：

```yaml
dispatch_log:
  started_at: ""
  dispatch_request: {}
  dispatch_decision: {}
  invocation:
    invoked: true
    method: ""
    target: ""
    result_status: success | failed | skipped
  recovery:
    result_recovered: true
    recovered_as:
      - sources[]
      - evidence[]
  boundaries: []
```

如果 adapter 没有真实执行 dispatch，只能输出：

```yaml
dispatch_log:
  invocation:
    invoked: false
  status: not_executed
```

## Result Recovery

`source-acquisition` 必须回收到：

```yaml
sources:
  - title: ""
    url: ""
    source_type: ""
    summary: ""
    reliability: low | medium | high
    freshness: ""
    extracted_at: ""
gaps: []
```

同时映射到 think-tank 输出：

```yaml
evidence:
  - ""
boundaries:
  - ""
```

## 状态判定

```yaml
verified:
  meaning: adapter 输出 dispatch_decision，真实调用 skill/tool，并回收 sources[] 与 evidence[]

verified_partial:
  meaning: 真实调用 skill/tool，但 dispatch_decision 或 recovery 仍是人工整理

mock:
  meaning: 只列出映射或模拟 dispatch，没有真实调用

blocked:
  meaning: 因环境、权限或缺少 skill 无法执行
```

## 禁止声明

- 不得把直接 WebFetch 调用称为完整 adapter dispatch，除非输出了 `dispatch_decision` 和 `dispatch_log`。
- 不得把 skill 存在称为 skill 已执行。
- 不得把手工整理的 sources 称为自动 result recovery。
- 不得把单 agent 执行称为真实多 agent runtime。

## 下一次验证标准

Claude Code 若要保持 `capability_auto_mapping: verified_partial_pre_invocation_decision`，必须至少包含：

```yaml
required_output:
  - dispatch_request
  - dispatch_decision
  - dispatch_log
  - sources
  - evidence
  - boundaries
```

## 当前验证状态

```yaml
dispatch_contract_validation:
  status: verified_partial_pre_invocation_decision
  evidence: think-tank/examples/claude-code-dispatch-pre-invocation-validation.md
  passed:
    - dispatch_request_present
    - dispatch_decision_present_before_invocation
    - dispatch_log_present
    - WebFetch_invoked
    - sources_present
    - evidence_present
  remaining_gaps:
    - full_adapter_runtime_not_verified
    - automatic_result_recovery_contract_not_verified
    - fallback_not_verified
```
