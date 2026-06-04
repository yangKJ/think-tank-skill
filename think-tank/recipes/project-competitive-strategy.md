# Project Competitive Strategy Recipe

```yaml
intent: project_competitive_strategy
default_mode: strategy
core_question: "当前项目真实具备什么能力、竞品为什么强、项目应从哪里切入市场？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `分析这个项目并和竞品对比`
- `项目竞品分析`
- `和已有 App 做对比`
- `我们的出路是什么`
- `怎么抢他们的市场`
- `项目定位和竞品策略`
- `产品差异化策略`

## Defaults

```yaml
profiles:
  - source-collector
  - product-strategist
  - trend-analyst
  - skeptic
  - report-architect
capabilities:
  - source-acquisition
  - knowledge-persistence
optional_peer_skills:
  - web-access
  - summarize
  - social-media-analyzer
  - obsidian
# Provider selection is configured in .think-tank/provider-policy.yaml
fallback_inputs:
  - local_files
  - user_provided_materials
  - public_web_sources
  - model_reasoning_with_boundaries
```

## Runtime Provenance

```yaml
runtime_provenance:
  think_tank_runtime_used: "{true|false}"
  provider_policy_checked: "{true|false}"
  dispatch_decision_emitted: "{true|false}"
  provider_invoked: "{true|false}"
  result_recovered: "{true|false}"
  true_multi_agent_runtime: "{true|false}"
  execution_method: "{full_runtime|adapter_runtime|direct_tool_call|single_agent_multi_profile|manual_synthesis|protocol_only}"
  data_collection: "{provider_managed|direct_assistant_tool|user_provided|local_files|none}"
  evidence_state: "{selected|invoked|recovered|verified_partial|verified|blocked|failed|tracking}"
  result_recovery: "{automatic|manual|none}"
  boundaries: []
```

## Required Inputs

```yaml
project:
  path: "<local project path or project description>"
  known_goal: "<optional>"
competitors:
  - name: "<competitor or alternative>"
    source_hint: "<optional url/app store/site>"
focus:
  - positioning
  - capability_gap
  - user_workflow
  - differentiation
  - market_entry
constraints:
  - readonly_project_scan
  - public_sources_only
```

## Required Analysis

1. 项目真实能力盘点：从本地代码、文档或用户材料识别已经存在的能力，避免把愿景当事实。
2. 竞品公开资料收集：官网、商店页、公开评论、新闻或公开文档优先；缺少来源时必须标注。
3. 用户和工作流对比：比较目标用户、核心场景、工作流深度、付费动力和迁移成本。
4. 差异化判断：说明当前项目不该正面硬刚什么，应从哪里切入。
5. 市场进入策略：输出短期可执行切口、中期产品闭环、长期护城河。
6. 证据边界：区分本地事实、外部事实、推理和未验证数据。
7. 产物沉淀：如用户要求写入项目，遵守 `protocol/artifact-write-policy.md`。
8. 行动转化：输出 `strategy_to_backlog`，遵守 `protocol/strategy-to-backlog.md`。

## Evidence Sources

必须按 `protocol/evidence-sources.md` 输出统一证据表：

```yaml
evidence_sources:
  local_code: []
  local_docs: []
  web_sources: []
  user_provided: []
  inference: []
  unavailable_data: []
```

## Artifact Output

如果用户要求沉淀到项目，必须先形成 artifact plan：

```yaml
artifact_plan:
  write_requested_by_user: true
  destination: "<project docs path or .think-tank/artifacts>"
  overwrite_existing: false
  git_impact: "new_file|modified_file|none"
  private_data_check: true
```

## Output

```text
runtime_provenance
结论
项目真实能力
竞品对比
差异化切口
市场进入策略
证据和来源
strategy_to_backlog
分歧与风险
边界
artifact_plan（如需要写入）
```

## Quality Gates

- 不把本地文档愿景当作当前实现事实。
- 不把公开营销话术当作竞品真实效果。
- 不把 direct tool call 写成 provider-managed full runtime。
- 不把 single agent 多 profile 写成真实并行专家团队。
- 竞品收入、留存、下载量、转化率等缺少可靠来源时必须进入 `unavailable_data`。
- 写入项目目录前必须声明路径、覆盖行为、Git 影响和隐私检查。
- backlog 必须包含优先级、验收标准和非目标。

## Non-goals

- 不替代正式市场调研、用户访谈或商业尽调。
- 不默认抓取登录态、私有数据、付费数据或社交平台敏感内容。
- 不默认修改目标项目代码。
