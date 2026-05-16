# registries

`leader-runtime/registries/` 存放主 agent 领导者系统的专家编制数据。

这里的 registry 是组织资产，不是一次运行的临时结果：

- `global-experts.yaml` 定义全局专家池。
- 项目级 team pack 只能裁剪或覆盖全局专家语义，不能重新定义全局专家身份。
- runtime 读取 registry 后再生成 dispatch decision、expert task packet 和 acceptance report。

边界：

- registry selection 不等于 expert invocation。
- registry availability 不等于真实 subagent 已调用。
- 专家定义可以被项目裁剪，但最终验收权仍属于 leader。
