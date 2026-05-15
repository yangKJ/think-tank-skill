# Evidence Sources

`evidence_sources` 是 think-tank 对证据来源的统一披露结构。它用于区分本地事实、外部事实、用户输入、推理判断和未验证数据。

## Goal

```yaml
feature: evidence_sources
scope: research_strategy_review_council_outputs
purpose: prevent_mixing_facts_sources_and_inference
```

## Required Structure

```yaml
evidence_sources:
  local_code:
    - path: "<repo-relative or absolute path>"
      claim: "<what this file supports>"
      evidence_state: verified_partial
  local_docs:
    - path: "<repo-relative or absolute path>"
      claim: "<what this document supports>"
      evidence_state: verified_partial
  web_sources:
    - url: "<public url>"
      title: "<page title or source name>"
      claim: "<what this source supports>"
      evidence_state: verified_partial
  user_provided:
    - material: "<description>"
      claim: "<what the user supplied>"
      evidence_state: recovered
  inference:
    - claim: "<reasoned conclusion>"
      based_on:
        - "<source id or summary>"
      confidence: low | medium | high
  unavailable_data:
    - item: "<data not available>"
      impact: "<how this limits the conclusion>"
      required_for_full_verification: true | false
```

## Rules

- `local_code` 只能用于真实读取过的代码文件。
- `local_docs` 只能用于真实读取过的项目文档。
- `web_sources` 只能用于真实访问过或由平台 provider 返回的公开资料。
- `user_provided` 必须说明材料来自用户，不得伪装成已独立核验。
- `inference` 必须引用它依赖的事实来源或说明基于哪些观察。
- `unavailable_data` 必须列出缺失项对结论强度的影响。

## Evidence State

证据状态必须使用 `protocol/capability-evidence-state-machine.md` 中的状态词。复杂报告通常只能声明 `verified_partial`，除非每个关键事实都有可重复来源和回收记录。

## Quality Gates

```yaml
local_facts_not_mixed_with_inference: true
web_claims_have_urls: true
missing_data_is_explicit: true
project_docs_not_treated_as_runtime_truth_without_code_check: true
```
