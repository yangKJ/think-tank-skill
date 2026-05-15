# Artifact Write Policy

think-tank 可以生成报告、运行记录、backlog 候选和验证计划，但写入项目目录必须遵守明确策略。默认情况下，think-tank 不应把临时分析直接写入目标项目。

## Goal

```yaml
feature: artifact_write_policy
scope: reports_backlogs_validation_plans_run_records
default_write_target: .think-tank/artifacts
```

## Destinations

```yaml
destinations:
  run_record:
    path: ".think-tank/runs/<run-id>.json"
    git_default: ignored
  temporary_artifact:
    path: ".think-tank/artifacts/<artifact-name>"
    git_default: ignored
  project_document:
    path: "<project>/Docs/<name>.md"
    requires_user_request: true
  public_skill_asset:
    path: "think-tank/<protocol|recipes|examples|schemas>/..."
    requires_repo_relevance: true
```

## Required Plan Before Writing

```yaml
artifact_plan:
  write_requested_by_user: true | false
  destination: "<path>"
  artifact_type: report | backlog | validation_plan | run_record | sample | protocol_doc
  overwrite_existing: true | false
  git_impact: new_file | modified_file | none
  private_data_check: true | false
  source_summary:
    - "<what evidence or inputs are included>"
  excluded_materials:
    - "<private or irrelevant materials intentionally excluded>"
```

## Rules

- 写入目标项目目录前，用户必须明确要求或确认。
- 不得默认覆盖已有项目文档。
- 不得把私有记忆、商业闭源核心、账号信息、未授权素材写入公开 Skill 资产。
- `.think-tank/` 是本地实例工作区，适合保存运行记录、临时产物和项目私有 policy。
- `think-tank/` 是公开 Skill 主体，只能放平台无关协议、recipe、schema、模板和公开安全样例。
- 若目标项目已有未提交修改，必须避免混入无关变更，并在最终说明中区分本次新增文件。

## Quality Gates

```yaml
write_path_declared: true
overwrite_behavior_declared: true
git_impact_declared: true
privacy_check_declared: true
project_private_data_not_added_to_public_skill: true
```
