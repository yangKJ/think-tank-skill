# Skill Invocation Contract

The invocation contract is the minimal structure an agent should form before
using `think-tank` for non-trivial work.

It prevents accidental over-claiming, hidden provider assumptions, and excessive
context loading.

## When To Emit

Emit the contract when:

- the user explicitly asks to use `think-tank`
- the task needs research, review, council, or strategy mode
- optional provider routing may happen
- the agent is about to load multiple protocol, platform, or provider files
- the output may become a run record, artifact, memory candidate, or backlog
  candidate

For tiny tasks, a compact `skill_route_decision` is enough.

## Input Contract

```yaml
think_tank_invocation:
  user_goal:
  available_context:
    user_supplied:
    local_files:
    web_required: true | false
    prior_run_required: true | false
  mode_hint: research | council | review | strategy | unknown
  output_expectation:
    format:
    depth:
    decision_needed: true | false
  constraints:
    time:
    privacy:
    platform:
    no_go_areas:
  provider_permissions:
    allow_network: true | false | unknown
    allow_browser: true | false | unknown
    allow_file_write: true | false | unknown
    allow_external_login: true | false | unknown
  policy_state:
    user_yaml_loaded: true | false
    trigger_source: user_policy | inferred_intent | explicit_user_request | none
    provider_policy_loaded: true | false
  progressive_disclosure_refs:
    - SKILL.md
```

## Output Contract

The final answer or artifact should be traceable to:

```yaml
think_tank_result:
  selected_intent:
  selected_mode:
  selected_recipe:
  selected_profiles:
  selected_capabilities:
  loaded_refs:
  invoked_providers:
  not_invoked_providers:
  evidence_state:
  execution_method:
  boundaries:
  conclusion:
  evidence:
  disagreements:
  risks:
  recommended_actions:
```

## Provider Boundary

Provider routing is allowed only after the agent can distinguish:

```yaml
route_selected:
provider_preflight:
dispatch_decision:
invoked_providers:
not_invoked_providers:
recovery:
verification_status:
```

If the agent only selected a provider pattern, it must not describe that
provider as invoked.

## Policy Boundary

Trigger words and provider preferences come from user-owned YAML policy or a
platform adapter. If no policy is loaded, the agent may infer intent from the
user request, but must disclose:

```yaml
policy_source: protocol_default
trigger_status: inferred_intent_only
```

## Minimal Contract Example

```yaml
think_tank_invocation:
  user_goal: "Review a release plan and identify blockers."
  mode_hint: review
  provider_permissions:
    allow_network: false
    allow_browser: false
    allow_file_write: false
    allow_external_login: false
  policy_state:
    user_yaml_loaded: false
    trigger_source: explicit_user_request
    provider_policy_loaded: false
  progressive_disclosure_refs:
    - SKILL.md
    - protocol/skill-trigger-intelligence.md
    - protocol/progressive-disclosure.md
```
