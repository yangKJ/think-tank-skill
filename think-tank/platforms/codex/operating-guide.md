# Codex Operating Guide

本文定义 think-tank 在 Codex 作为主平台时的日常运行方式。

Codex 是当前优先验证和使用平台。Claude Code 仍是目标平台之一，但在 Codex foundation 稳定之前，不作为主线推进。

## 默认执行姿态

```yaml
platform: codex
default_execution: single_agent_multi_profile
core_protocol: think-tank/protocol
primary_adapter: think-tank/platforms/codex
status: verified_foundation
```

Codex 默认不声称真实多 agent。除非用户明确要求并授权使用 subagent，否则 think-tank 在 Codex 中按“单 agent 多 profile 分段执行”处理。

## 本地工作区

Codex 项目本地 think-tank 数据统一放在：

```text
.think-tank/
```

其中：

```text
.think-tank/provider-policy.yaml  # 项目触发词和 provider 偏好
.think-tank/memory/               # 项目本地记忆
.think-tank/runs/                 # 运行记录
.think-tank/artifacts/            # 产物
```

`.think-tank/` 默认应被 Git 忽略。公开 Skill 源 `think-tank/` 不存放项目实例配置。

本地 `provider-policy.yaml` 是 overlay，不是完整替换。Codex 先加载公开默认 policy，
再合并 `.think-tank/provider-policy.yaml`，这样项目定制不会丢失基础
research、council、review 和 strategy 路由。

## 触发方式

用户可以直接用自然语言触发 think-tank，不需要写完整协议字段。

推荐触发语：

```text
用 think-tank research mode 调研……
用 think-tank council mode 讨论……
用 think-tank review mode 审查……
用 think-tank strategy mode 制定路线……
用 think-tank 帮我判断……
```

如果用户没有显式指定 mode，Codex adapter 按 `protocol/mode-selection.md` 自动选择。

旧 research agent 的触发词迁移见：

```text
platforms/codex/trigger-routing.md
```

因此用户继续说“研究一下”“深度研究”“竞品分析”“舆情分析”“开会讨论”时，Codex 应先路由到 think-tank，再按 capability slots 选择 `.codex/skills/` 下的同级工具 skill。不能因为旧触发词命中某个旧工作流 skill，就绕过 think-tank 主协议。

## 执行步骤

Codex 执行 think-tank 时应按以下顺序：

1. 识别用户目标和成功标准。
2. 选择 mode。
3. 选择 profiles。
4. 选择 capabilities。
5. 判断每个 capability 是否有当前可用实现。
6. 收集本地、用户提供或可用工具证据。
7. 分 profile 输出独立判断。
8. 合并分歧、风险和共识。
9. 输出结论和行动建议。
10. 标注边界和验证状态。

## 能力状态规则

```yaml
verified:
  meaning: 当前 Codex 环境真实执行并回收结果
verified_optional:
  meaning: 可选能力在受控范围验证过，不是最低依赖
degraded:
  meaning: capability 被选择，但当前没有可用实现，转为用户材料或本地材料分析
planned:
  meaning: 文档定义存在，但当前未执行
```

Codex 输出必须避免：

- 把 `degraded` 写成 `verified`。
- 把 Browser localhost fixture 写成通用网页浏览。
- 把单 agent profile simulation 写成真实多 agent。
- 把 capability 文件存在写成外部 skill 已安装。

## 最小安装默认行为

只安装 think-tank 时，Codex 可以执行：

- 协议选择
- mode 选择
- profile 模拟
- 本地仓库读取
- 用户提供材料分析
- 结构化输出
- 边界声明

不能默认执行：

- 外部网页浏览
- 视频下载
- 音频转录
- 社媒抓取
- Obsidian 写入
- Claude Code subagent 调度

## 输出骨架

Codex 日常输出建议使用：

```text
结论
依据
角色观点
分歧与风险
行动建议
边界
```

轻量任务可以压缩，但不能省略结论、风险和下一步。

## 何时需要工具

Codex adapter 应先判断工具是否真的必要。

```yaml
local_files_needed:
  use: shell_reading
  examples:
    - rg
    - sed
    - git status

browser_needed:
  use: browser-automation
  condition: 用户需要验证页面、DOM、交互或视觉状态

network_needed:
  use: web/source-acquisition
  condition: 用户需要最新信息或外部来源

private_tool_needed:
  use: optional capability
  condition: 用户明确授权并且工具可用
```

## 验收命令

Codex foundation 当前使用三条命令验收：

```bash
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/schema_sample_check.py
```

新增 Codex 平台文档或验证产物后，应更新检查脚本。

## 当前停止点

Codex 主平台当前已达到 Claude Code preflight 前的停止点：

```yaml
codex_readiness_matrix: ready_before_claude_code_preflight
next_platform: claude-code
stop_reason: Codex foundation 和日常使用路径已完成，后续差异属于 Claude Code runtime 验证
```
