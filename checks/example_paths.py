"""解析 examples 分层后的公开样例路径。"""

from __future__ import annotations

from pathlib import Path


def resolve_example_path(root: Path, path: Path) -> Path:
    """把旧的 think-tank/examples/<name> 路径解析到分层后的样例。

    历史检查脚本直接引用 `think-tank/examples/` 根目录下的文件。
    现在公开样例已经按用途分组；为了让检查聚焦契约有效性而不是目录
    搬迁，通过 examples 树中的唯一文件名解析缺失的旧路径。
    """
    examples_root = root / "think-tank" / "examples"
    if path.exists() or path.parent != examples_root:
        return path
    matches = sorted(examples_root.rglob(path.name))
    if len(matches) == 1:
        return matches[0]
    return path
