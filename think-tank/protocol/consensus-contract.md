# Consensus Contract

本文定义 think-tank v0.2 的 deliberation / consensus contract。

它吸收旧 research think-tank `consensus.py` 的显式投票和 blocking objection 经验。

## 目的

consensus contract 用于避免多角色讨论变成简单并列观点，确保分歧、反对意见和停止条件可审计。

## Position

每个参与角色应给出结构化 position：

```yaml
position:
  profile: ""
  proposal: ""
  evidence: []
  risks: []
  objections: []
  vote:
    main: agree | disagree | abstain
  confidence: low | medium | high
```

## Vote Options

```yaml
vote_options:
  - agree
  - disagree
  - abstain
```

## Blocking Objection

blocking objection 成立条件：

```yaml
blocking_objection:
  required_fields:
    - objections
    - vote.main: disagree
  consequence:
    - cannot_mark_L1_consensus
    - must_record_minority_opinion
    - must_trigger_additional_round_or_L3_adjudication
```

## Consensus Levels

```yaml
L1:
  meaning: executable consensus
  conditions:
    - agreement_rate >= threshold
    - no_blocking_objection

L2:
  meaning: unresolved but negotiable disagreement
  action: continue_targeted_round

L3:
  meaning: timeout_or_low_consensus_or_max_rounds
  action: facilitator_adjudication_with_minority_record
```

## Continue / Stop Conditions

```yaml
continue_when:
  - agreement_rate < threshold
  - blocking_objection_present
  - evidence_gap_blocks_decision
  - current_round < max_rounds

stop_when:
  - L1_consensus
  - max_rounds_reached
  - timeout
  - user_interrupt
  - facilitator_adjudication
```

## Quality Gate

最终输出必须包含：

- agreed points
- disputed points
- blocking objections
- minority opinion
- confidence
- why stop now

## Verification Status

```yaml
consensus_contract_v0_2: specified
explicit_vote_runtime: planned
single_agent_multi_profile_simulation: verified
true_multi_agent_consensus_runtime: planned
```
