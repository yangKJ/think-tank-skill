# Capability Slot Contract

本文定义 think-tank v0.2 的 capability slot 契约。

它吸收旧 research think-tank `slot_resolver.py` 和 `slot_validator.py` 的经验，但不继承旧 `skill.yaml` 作为配置中心。

## 目的

capability slot 负责说明任务需要什么能力，而不是规定必须使用哪个工具。

## Slot Types

```yaml
slot:
  name: source-acquisition
  required: true | false
  candidates: []
  fallback: degrade | stop | ask_user
  status: verified | verified_partial | mock | tracking | planned | unavailable
```

## Required Slot

required slot 缺失时：

- 不得继续声称完整执行。
- 必须输出缺失能力。
- 必须说明降级后哪些结论不可验证。
- 可以进入 partial output。

## Optional Slot

optional slot 缺失时：

- 可以继续执行。
- 必须在 boundaries 中说明能力缺口。
- 不得把 optional 缺失写成 failure，除非用户任务依赖该能力。

## Resolution Flow

```text
runtime_plan
  -> required_slots
  -> optional_slots
  -> platform_adapter_mapping
  -> availability_check
  -> selected_implementation
  -> capability_status
```

## Validation Rules

```yaml
rules:
  - required slot must have at least one available implementation or explicit degradation
  - optional slot may be omitted with boundary
  - installed tool does not equal verified capability
  - direct tool invocation does not equal full adapter runtime
  - failed invocation must not fabricate sources or evidence
```

## Output Fields

每次 capability 调用应输出：

```yaml
capability_resolution:
  capability: ""
  required: true
  candidate_implementations: []
  selected_implementation: ""
  availability: available | unavailable | unknown
  invocation_status: success | failed | skipped
  capability_status: verified | verified_partial | unavailable
  boundary: ""
```

## Platform Examples

```yaml
# 以下为示例，非协议规范。实际 provider 选择由本地 policy 配置决定。
claude_code:
  source-acquisition:
    candidates:
      - builtin web fetch (platform-native)
      - browser automation provider
      - AI-enhanced search provider

codex:
  source-acquisition:
    candidates:
      - local static reader (platform-native)
      - web run provider
      - user-provided material
```

## Verification Status

```yaml
slot_contract_v0_2: specified
source_acquisition_slot: verified_partial
browser_automation_slot: planned
knowledge_persistence_slot: planned
media_processing_slot: planned
social_listening_slot: planned
```
