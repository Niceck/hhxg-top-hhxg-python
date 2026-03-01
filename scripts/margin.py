#!/usr/bin/env python3
"""融资融券数据 — 近 7 日余额变化、净买入排名。

Usage:
    python3 margin.py           # 完整报告
    python3 margin.py overview  # 市场总览
    python3 margin.py top       # 净买入/净卖出 TOP
    python3 margin.py --json    # JSON 原始输出

数据来源: https://hhxg.top
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import fetch_json, print_cache_hint, run_main


def _fetch():
    return fetch_json("assistant/recent_margin_7d.json", "margin_7d.json")


# ── Formatters ──────────────────────────────────────────────


def fmt_overview(data):
    mkt = data.get("market", {})
    win = data.get("window", {})
    lines = [
        "# 融资融券市场总览（近 7 个交易日）",
        "",
        "区间: %s ~ %s" % (win.get("start", "?"), win.get("end", "?")),
        "",
    ]
    totals = mkt.get("daily_totals", [])
    if totals:
        latest = totals[-1]
        lines.append("最新融资余额: **%.0f 亿**" % latest.get("rzye_yi", 0))
        lines.append("最新融券余额: **%.1f 亿**" % latest.get("rqye_yi", 0))
        lines.append("")

    delta_rz = mkt.get("delta_rzye_yi", 0)
    delta_rq = mkt.get("delta_rqye_yi", 0)
    sign_rz = "+" if delta_rz > 0 else ""
    sign_rq = "+" if delta_rq > 0 else ""
    lines.append("7 日融资变化: **%s%.1f 亿**" % (sign_rz, delta_rz))
    lines.append("7 日融券变化: **%s%.1f 亿**" % (sign_rq, delta_rq))
    lines.append("")

    # 每日余额趋势
    if totals:
        lines.append("### 每日余额")
        lines.append("| 日期 | 融资余额(亿) | 融券余额(亿) |")
        lines.append("|------|-------------|-------------|")
        for t in totals:
            lines.append("| %s | %.0f | %.1f |" % (
                t.get("date", ""), t.get("rzye_yi", 0), t.get("rqye_yi", 0)
            ))

    return "\n".join(lines)


def fmt_top(data):
    top = data.get("top", {})
    lines = ["# 融资净买入/净卖出 TOP", ""]

    inc = top.get("increase_rzye", [])
    if inc:
        lines.append("## 融资净买入 TOP")
        lines.append("| 股票 | 最新余额(亿) | 变化(亿) | 变化% |")
        lines.append("|------|-------------|---------|-------|")
        for s in inc[:10]:
            lines.append("| %s | %.1f | +%.1f | +%.1f%% |" % (
                s.get("name", ""), s.get("latest_rzye_yi", 0),
                s.get("delta_rzye_yi", 0), s.get("delta_pct", 0),
            ))

    dec = top.get("decrease_rzye", [])
    if dec:
        lines.append("")
        lines.append("## 融资净卖出 TOP")
        lines.append("| 股票 | 最新余额(亿) | 变化(亿) | 变化% |")
        lines.append("|------|-------------|---------|-------|")
        for s in dec[:10]:
            lines.append("| %s | %.1f | %.1f | %.1f%% |" % (
                s.get("name", ""), s.get("latest_rzye_yi", 0),
                s.get("delta_rzye_yi", 0), s.get("delta_pct", 0),
            ))

    return "\n".join(lines)


def fmt_all(data):
    return fmt_overview(data) + "\n\n---\n\n" + fmt_top(data)


SECTIONS = {"all": fmt_all, "overview": fmt_overview, "top": fmt_top}


def main():
    section, _, use_json = run_main(SECTIONS)
    try:
        data, cached = _fetch()
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    print_cache_hint(cached, data.get("window", {}).get("end", ""))
    if use_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(SECTIONS[section](data))


if __name__ == "__main__":
    main()
