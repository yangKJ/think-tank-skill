# Codex Adapter

该目录定义 think-tank 在 Codex 中的适配方式。

## 职责

- 把 `protocol/` 映射为 Codex 可执行的协作流程
- 定义何时使用本地工具、shell、文件读写和浏览能力
- 定义 Codex 中的角色模拟、子任务拆解和结果汇总方式
- 定义工作区文件、记忆和输出的保存边界
- 明确 Codex 适配不能改变 think-tank 主协议

## 初始执行方式

Codex 适配可以先以单 agent 协议执行为主：

1. 解析任务和 mode
2. 按角色顺序生成独立观点
3. 使用本地仓库和工具收集证据
4. 汇总分歧、风险和行动建议
5. 执行质量门禁

如果后续使用 Codex subagent 或并行代理能力，应在本目录单独记录能力边界。

## 后续文件规划

- `adapter.md`：Codex 适配协议
- `capability-mapping.md`：Codex 工具到 think-tank capabilities 的映射
- `capability-status.md`：Codex 主平台 capability 当前状态
- `minimal-runtime.md`：Codex minimal runtime mirror 说明
- `operating-guide.md`：Codex 日常运行手册
- `runtime/source_acquisition_minimal.py`：source-acquisition 最小参考 runner
- `runtime/pipeline.py`：Codex runtime pipeline，串联 planner、slot resolver、state model、source acquisition 和 consensus
- `smoke-test.md`：Codex 平台 smoke test 定义
- `task-templates.md`：Codex 用户任务模板

## Local Workspace

Codex 项目本地配置应放在：

```text
.think-tank/
```

推荐本地 provider policy 路径：

```text
.think-tank/provider-policy.yaml
```

`.codex/skills/think-tank` 可以是指向公开 `think-tank/` 的安装入口，但项目实例配置不应写入 Skill 源目录。

本地 provider policy 默认作为 overlay 合并到公开 example policy 上。项目只需要写自己的
触发词、优先级和 provider 偏好，不需要复制整份默认路由。
