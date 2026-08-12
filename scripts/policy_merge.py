#!/usr/bin/env python3
"""按低到高优先级合并 JSON Policy，并记录覆盖来源。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def deep_merge(dst: dict[str, Any], src: dict[str, Any], source: str, path: tuple[str, ...], log: list[dict[str, Any]]) -> None:
    """递归合并字典；标量覆盖时记录旧值和来源。"""
    for key, value in src.items():
        p = path + (key,)
        if isinstance(value, dict) and isinstance(dst.get(key), dict):
            deep_merge(dst[key], value, source, p, log)
            continue
        if key in dst and dst[key] != value:
            log.append({"path": ".".join(p), "old": dst[key], "new": value, "source": source})
        dst[key] = value


def main() -> int:
    """CLI 入口；参数顺序即低到高优先级。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("policies", nargs="+", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    merged: dict[str, Any] = {}
    log: list[dict[str, Any]] = []
    for path in args.policies:
        obj = json.loads(path.read_text(encoding="utf-8"))
        deep_merge(merged, obj, path.name, (), log)
    result = {"effective": merged, "overrides": log}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
