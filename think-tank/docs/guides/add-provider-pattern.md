# Add Provider Pattern

Provider patterns must stay optional and evidence-bounded.

Required fields:

```yaml
route_selected:
provider_preflight:
dispatch_decision:
invoked_providers:
not_invoked_providers:
recovery:
boundaries:
verification_status:
```

Also update:

- `provider-integration-patterns.md`
- `provider-test-matrix.md`
- `examples/provider-patterns/`
- `examples/provider-ledgers/`
- relevant checks
