# Codex Leader Orchestration Blueprint

本文定义 `leader-runtime/` 在 Codex 平台上的主线：把主 agent 从执行者升级为领导者，并让其组织一批专家 agent 完成任务。

它不是 `think-tank` 的 Skill core 文档，而是主 agent 领导者系统的母规范。

## 结论

Codex 主 agent 的目标身份，不应停留在：

- 会做研究的高阶 Skill 使用者
- 会调用一些能力槽的 orchestrator
- 会扮演多个 profile 的强主 agent

而应升级为：

```yaml
leader_identity:
  role: organization_leader
  authority: highest_within_runtime_scope
  default_scope: full_expert_pool
  responsibilities:
    - decide_mode
    - select_roles
    - choose_dispatch_path
    - assign_experts
    - enforce_acceptance
    - arbitrate_disagreement
    - synthesize_final_decision
```

## 为什么要在 Codex 平台这样做

### 原因 1: Codex 的主 agent 已经足够强

Codex 主 agent 已经具备：

- 强任务理解与收敛能力
- 强本地代码执行和修改能力
- 强工具使用与验证能力
- 强最终集成能力

继续提升上限的重点，不该只是让主 agent 亲自做更多，而应该让它组织更多高质量分工。

### 原因 2: Codex 更适合作为验收中枢

Codex 的优势不只是角色化表达，还包括：

- 直接读代码、跑命令、看差异
- 把专家建议拉回到仓库事实和执行结果
- 在派发后承担真实最终仲裁

### 原因 3: 未来不只需要一个项目级主 agent

你的目标不是只增强当前仓库，而是让其他 Codex 项目的主 agent 也升级为领导者。

因此需要一层高于 `think-tank` 的运行系统，专门承载：

- 主 agent 身份
- 专家组织
- 项目派生
- 派遣和验收

## 为什么不能继续放在 think-tank core

`think-tank/` 的定位仍然是：

- 高阶 Skill
- 跨平台协议源
- 可被不同主 agent 调用的认知能力层

如果把主 agent 领导者系统继续塞进 `think-tank/`，会带来两个问题：

1. `think-tank` 会从 Skill core 漂移成平台级主 agent 操作层。
2. Codex 平台私有的 leader 机制会反过来污染跨平台 Skill 抽象。

因此必须分层：

```text
think-tank/
  -> 高阶 Skill core

leader-runtime/
  -> 主 agent 领导者系统
```

## 组织分层

### Layer 1: leader-runtime 母体领导者

```yaml
leader_class:
  id: think_tank_global_leader
  scope: cross_project
  expert_pool_access: full
  responsibilities:
    - define_orchestration_rules
    - maintain_role_registry
    - define_dispatch_contract
    - define_acceptance_contract
    - provide_project_templates
```

### Layer 2: 项目派生领导者

```yaml
project_leader:
  inherits_from: think_tank_global_leader
  expert_pool_access: subset
  restrictions:
    - limited_by_project_domain
    - limited_by_project_tools
    - limited_by_project_risk
```

### Layer 3: 专家执行层

```yaml
expert_agent:
  role_type: domain_specialist | reviewer | builder | operator | strategist
  authority: delegated
  output_contract: role_result
  final_decision_authority: false
```

## 优势

- 主上下文更干净
- 专业视角更稳定
- 项目可裁剪、体系可复用
- 验收能力更强
- 更适合复杂任务

## 代价和缺点

- 系统复杂度显著上升
- 容易出现伪多 agent
- leader 容易退化成中转站
- 初期建设成本高
- 失败会被放大

## 设计取舍

```text
宁可少派发但可验收
也不要大规模派发却不可控
```

```text
宁可明确 fallback
也不要把单上下文模拟包装成真实专家组织
```

```text
宁可先把 leader-runtime 做成母体领导者
再让其他项目继承
也不要每个项目各自摸索一套不兼容的组织方式
```

## Codex 领导者编排模型

```text
user request
  -> leader intake
  -> intent / mode / recipe selection
  -> dispatch decision
  -> expert selection
  -> task packet generation
  -> expert execution
  -> role-result recovery
  -> acceptance / retry / arbitration
  -> final synthesis
```

### Leader Intake

```yaml
selected_intent:
selected_mode:
selected_recipe:
leader_execution_decision:
selected_roles:
selected_experts:
dispatch_strategy:
acceptance_owner: leader
```

### Dispatch Decision

```yaml
dispatch_decision:
  task_shape: simple | focused | multi_domain | adversarial | execution_heavy
  delegation_needed: true | false
  reason:
  selected_path:
  fallback_path:
  verification_status:
```

### Expert Task Packet

```yaml
expert_task_packet:
  task_id: string
  leader_id: think_tank_global_leader | project_leader
  expert_id: string
  mapped_role: collector | domain_expert | skeptic | builder | synthesizer
  objective: string
  task_scope: string
  required_capabilities: []
  input_context: []
  deliverables: []
  acceptance_checks: []
  independence_boundary: string
  fallback_rule: string
```

### Acceptance Governance

```yaml
acceptance_contract:
  owner: leader
  checks:
    - schema_complete
    - evidence_present
    - boundary_declared
    - claim_traceable
    - no_over_authority
  retry_limit: 2
  escalation_path:
    - re-dispatch
    - narrower_scope
    - downgrade_runtime
    - final_manual_arbitration
```

## 与 think-tank 的关系

`leader-runtime` 不替代 `think-tank`，而是编排它。

```text
leader-runtime
  -> 负责主 agent 身份、专家组织、项目派生、派遣与验收

think-tank
  -> 负责研究、审议、review、strategy 等高阶认知技能
```

## 当前状态

```yaml
leader_blueprint: specified
codex_dispatch_runtime_for_full_expert_pool: planned
expert_registry_materialization: implemented_partial
acceptance_governance_runtime: implemented_partial
project_derived_leader_model: planned
```
