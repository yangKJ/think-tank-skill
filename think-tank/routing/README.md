# Routing Layer

`routing/` 是 think-tank 的中间连接层。

它解决的问题是：

```text
用户请求进入 policy / intent / recipe / capability 后，
如何选择、调用、降级和回收外部 peer skill？
```

## 定位

```yaml
layer: routing
purpose: connect_capabilities_to_optional_peer_skills
platform_neutral: mostly
owns_protocol: false
owns_peer_skills: false
think_tank_core_depends_on_peer_skills: false
```

## 与旧任务编排技能的关系

旧竞品分析编排技能同时承担了三件事：

1. 竞品分析任务配方。
2. 工具技能连接器。
3. 报告输出规范。

新 think-tank 拆成三层：

```text
routing/policy-schema.md
  -> 定义触发词、intent、recipe、capability 和 provider 偏好如何配置

recipes/competitive-intelligence.md
  -> 定义竞品分析任务应该怎么做

routing/skill-router.md
  -> 定义 capability 如何解析到候选 peer skills

platforms/<platform>/
  -> 定义具体平台如何真实调用、失败和回收结果
```

因此旧竞品分析编排职责已经被 routing policy 替代。竞品研究方法论已进入 recipe、template 或 domain pack，不再需要保留独立 peer skill。

## 文件

- `policy-schema.md`：定义触发词、intent、recipe、capability 和 provider 偏好的 YAML 配置结构。
- `skill-router.md`：从 intent/recipe/capability 到 peer skill candidates 的选择规则。
- `dispatch-policy.md`：什么时候允许调用 peer skill、什么时候降级、如何声明状态。
- `result-recovery.md`：peer skill 输出如何回收到 sources、evidence、role-result 和 final output。

## 最小路由链

```text
user request
  -> routing/policy-schema.md
  -> protocol/intent-routing.md
  -> recipes/<recipe>.md
  -> capabilities/<capability>.md
  -> routing/skill-router.md
  -> routing/dispatch-policy.md
  -> platforms/<platform>/...
  -> routing/result-recovery.md
  -> think-tank output
```

## 边界

Routing 层可以选择外部 peer skills，但不能：

- 要求某个 peer skill 必须存在。
- 把 peer skill 安装状态说成执行验证。
- 把平台 adapter 的实现细节写成协议。
- 绕过 think-tank 的 output 和 quality gates。
