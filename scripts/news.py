#!/usr/bin/env python3
"""实时财经快讯 — 最新新闻、按分类筛选。

Usage:
    python3 news.py            # 最新 20 条
    python3 news.py 50         # 最新 50 条
    python3 news.py --json     # JSON 原始输出

数据来源: https://hhxg.top/api/news（每小时滚动）；接口不可用或要超过 50 条时
读静态 news/n0.json（每天随全站构建更新 3 次）。
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import SITE_URL, fetch_json, print_cache_hint

API_MAX_LIMIT = 50


def _api_items(payload):
    data = payload.get("data") if isinstance(payload, dict) else None
    items = data.get("items") if isinstance(data, dict) else None
    return items if isinstance(items, list) else None


def _fetch(limit):
    """(条目列表, 是否缓存)：先读每小时滚动的 /api/news，不行再读静态 n0.json。

    接口这一路不写本地缓存：接口挂掉时直接改读静态（静态有自己的离线缓存），
    不会拿出一份旧的接口快照。
    """
    if limit <= API_MAX_LIMIT:
        try:
            payload, _ = fetch_json(f"{SITE_URL}/api/news?limit={max(limit, 1)}")
            items = _api_items(payload)
            if items is not None:
                return items, False
            print("快讯接口返回异常，改读静态数据", file=sys.stderr)
        except RuntimeError as e:
            # 只留原因的第一句：fetch_json 的 404 文案带「请升级技能」，对接口这一路是误导
            reason = str(e).splitlines()[0].split("，")[0]
            print(f"快讯接口不可用（{reason}），改读静态数据", file=sys.stderr)
    data, cached = fetch_json("news/n0.json", "news_latest.json")
    items = data if isinstance(data, list) else data.get("items", [])
    return items, cached


def fmt_news(items, limit=20):
    if not items:
        return "暂无快讯数据"
    lines = [f"# 财经快讯（最新 {min(limit, len(items))} 条）", ""]

    current_date = ""
    for n in items[:limit]:
        t = n.get("t", "")
        cat = n.get("cat", "")
        title = n.get("title", "")

        # 按日期分组
        date_part = t.split("T")[0] if "T" in t else ""
        if date_part != current_date:
            current_date = date_part
            lines.append("")
            lines.append(f"## {date_part}")

        time_part = t.split("T")[1][:5] if "T" in t else t
        tag = f"[{cat}]" if cat else ""
        lines.append(f"- `{time_part}` {tag} {title}")

    lines.append("")
    lines.append("---")
    lines.append("更多快讯 → https://hhxg.top/news.html")
    lines.append("量化选股 / 游资席位 / 策略回溯 → https://hhxg.top/xuangu.html")
    return "\n".join(lines)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = {a for a in sys.argv[1:] if a.startswith("-")}
    use_json = "--json" in flags

    limit = 20
    if args:
        try:
            limit = int(args[0])
        except ValueError:
            pass

    try:
        items, cached = _fetch(limit)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    print_cache_hint(cached, "")

    if use_json:
        print(json.dumps(items[:limit], ensure_ascii=False, indent=2))
    else:
        print(fmt_news(items, limit))


if __name__ == "__main__":
    main()
