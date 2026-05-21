# Contributing

感谢参与 think-tank 建设。这个仓库的目标不是堆叠脚本，而是维护一个跨平台、可复用的高阶 Skill 和统一协议。

## 核心原则

1. `think-tank/protocol/` 是唯一协议源。
2. `think-tank/platforms/` 只能做平台适配，不能重新定义协议。
3. `think-tank/modes/` 只能定义场景默认策略，不能变成平行产品。
4. 任何能力都必须标注真实状态：`verified`、`mock`、`tracking`、`planned`。

## 修改协议

修改 `think-tank/protocol/` 时，请同时检查：

- 是否改变了输入输出语义
- 是否影响 mode 选择
- 是否影响角色职责
- 是否影响质量门禁
- 是否需要更新 `CHANGELOG.md`
- 是否属于 `protocol/versioning.md` 中定义的 breaking change

## 新增 mode

新增 mode 时，至少应包含：

- 适用场景
- 不适用场景
- 默认角色
- 流程重点
- 输出重点
- 质量门禁
- 与历史体系或平台适配的关系

新增 mode 后，请更新：

- `think-tank/modes/README.md`
- `think-tank/protocol/mode-selection.md`
- `think-tank/examples/`

## 新增平台适配

新增平台适配时，至少应包含：

- `README.md`
- `adapter.md`
- 能力状态声明
- 执行模型
- 结果回收方式
- 平台限制

平台适配不能把平台特有能力写成协议要求。

## 提交前检查

运行：

```bash
python3 checks/protocol_check.py
```

检查通过后再提交。

