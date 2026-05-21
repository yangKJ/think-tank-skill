# Validation Tiers

本文把 `think-tank` 的检查分成三层，避免把本地 provider 验证误当成公开发布承诺。

## Tier 1: release gate

面向所有开源用户。只检查公开仓库可复现的协议、样例、隐私和发行边界。

```bash
python3 checks/open_source_release_suite.py
```

该 suite 覆盖：

- protocol integrity
- Codex foundation artifacts
- schema samples
- minimal runtime execution
- runtime provenance
- public package boundary
- release privacy
- open-source release copy

## Tier 2: core validation

面向维护者。用于协议、runtime、schema、routing、templates 或迁移文档发生变化时。

```bash
python3 checks/protocol_check.py
python3 checks/runtime_contract_check.py
python3 checks/runtime_result_schema_check.py
python3 checks/routing_layer_check.py
python3 checks/template_check.py
```

这层可以引用仓库内历史迁移材料，但不能要求用户拥有本地登录态、私有知识库或 provider 服务。

## Tier 3: local provider validation

面向当前机器或项目实例。只有存在 `.think-tank/`、`.codex/skills/`、登录态或本地服务时才运行。

示例：

```bash
python3 checks/codex_installed_skill_check.py
python3 checks/codex_external_skills_check.py
python3 checks/obsidian_knowledge_mode_check.py
python3 checks/ollama_service_decision_check.py
python3 checks/revieworg_provider_check.py
```

这层检查可以公开作为参考，但不能进入默认 release gate。通过它只代表当前项目实例可用，不代表开源用户默认可用。

## Reporting Rule

输出或发布文案必须写清：

```yaml
validation_tier: release_gate | core_validation | local_provider_validation
provider_invoked: true | false
result_recovered: true | false
verification_status: verified | verified_partial | planned | blocked | failed
```
