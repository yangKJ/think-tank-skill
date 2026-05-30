# Public Example: Research Request

## User Request

研究一下一个新开发工具是否值得引入团队，基于用户提供的 README、价格页摘录和两篇公开文章，输出采用建议。

## Expected think-tank Routing

```yaml
selected_intent: general_research
selected_mode: research
selected_recipe: evidence_synthesis
selected_profiles:
  - source-collector
  - trend-analyst
  - skeptic
selected_capabilities:
  - source-acquisition
skill_route:
  source-acquisition: user_provided_material
execution_method: single_agent_multi_profile_fallback
invoked_providers: []
not_invoked_providers:
  - web-access
  - browser-automation
  - private-knowledge-base
boundaries:
  - user-provided material only
  - no login, scraping, download, or private write
verification_status: verified_for_protocol_example
```

## Output Shape

```text
结论
依据
角色观点
分歧与风险
行动建议
边界
```

## Key Rule

If the assistant reads the provided files directly, report `data_collection: user_provided` or `local_files`; do not claim provider-managed source acquisition.
