# Release Tagging

本文定义 `think-tank` 公开仓库的版本和标签策略。

## Versioning Rule

```yaml
stable_major_series: 1.x
current_recommended_tag: v1.0.0
tag_format: vMAJOR.MINOR.PATCH
```

## Tag Meanings

- `v1.0.0`: 首个 stable release，代表 stable protocol surface + stable Codex-first public path
- `v1.0.x`: 文档修正、门禁修正、非破坏性样例补充
- `v1.1.0`: 新增已经证据化且默认公开承诺的能力
- `v2.0.0`: 协议、schema、默认行为或公开边界发生破坏性变化

## When To Cut A Patch Release

适用于：

- release gate 修正
- 隐私扫描规则补充
- README / support matrix / release notes 一致性修正
- 新增不改变默认承诺边界的验证样例

## When Not To Bump Minor

以下情况不应单独视为 `minor` 升级：

- 只是安装了更多 peer skills
- 只是 policy 可以选中更多 provider
- 只是新增了 `selected` / `planned` / `available_not_verified` 级别能力
- 只是存在新脚本，但没有形成公开稳定承诺

## Release Cut Checklist

```text
1. run open_source_release_suite
2. run stable_release_check
3. confirm no local path leaks
4. confirm README and support matrix match the actual claim
5. prepare GitHub Release from docs/v1.0.0-release-notes.md
6. then let the maintainer create the git tag manually
```

## Maintainer Reminder

- Codex 不负责执行远端发布动作
- `git tag`、`git push --tags`、GitHub Release 发布都应由仓库维护者手动完成

