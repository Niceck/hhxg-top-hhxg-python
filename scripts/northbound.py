#!/usr/bin/env python3
"""北向资金（沪深港通）— 近 7 日资金流向与活跃度。

Usage:
    python3 northbound.py           # 完整报告
    python3 northbound.py overview  # 7 日统计总览
    python3 northbound.py daily     # 每日明细表
    python3 northbound.py --json    # JSON 原始输出

数据来源: https://hhxg.top
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import as_dicts, fetch_json, print_cache_hint, run_main


def _fetch():
    return fetch_json("assistant/recent_northbound_7d.json", "northbound_7d.json")


def _f(v, fmt="{:.1f}"):
    """None 安全的数值格式化。"""
    if v is None:
        return "—"
    try:
        return fmt.format(float(v))
    except (TypeError, ValueError):
        return str(v)


_CALIBER_NOTE = (
    "> 口径说明：2024-08 起沪深港通接口口径变更，北向数值恒为正，\n"
    "> 仅反映外资成交活跃度，不代表真实净流入方向；南向为累计存量值。"
)


# ── Formatters ──────────────────────────────────────────────


def fmt_overview(data):
    win = data.get("window") or {}
    stats = data.get("stats") or {}
    lines = [
        "# 北向资金总览（近 7 个交易日）",
        "",
        "区间: {} ~ {}".format(win.get("start", "?"), win.get("end", "?")),
        "",
        "7 日北向合计: **{} 亿**".format(_f(stats.get("total_inflow_7d_yi"))),
        "日均: **{} 亿**".format(_f(stats.get("avg_daily_yi"))),
        "单日最高 / 最低: {} 亿 / {} 亿".format(
            _f(stats.get("max_single_day_yi")), _f(stats.get("min_single_day_yi"))
        ),
        "活跃天数: {} 天（窗口 {} 天）".format(
            stats.get("net_inflow_days", "?"), win.get("trading_days", "?")
        ),
        "",
        _CALIBER_NOTE,
    ]
    return "\n".join(lines)


def fmt_daily(data):
    series = as_dicts(data.get("series"))
    lines = ["# 沪深港通每日明细", ""]
    if not series:
        lines.append("暂无数据")
        return "\n".join(lines)

    lines.append("| 日期 | 北向(亿) | 沪股通(亿) | 深股通(亿) | 南向累计(亿) |")
    lines.append("|------|---------|-----------|-----------|-------------|")
    # series 按日期降序（最新在前），表格按时间正序展示
    for row in reversed(series):
        lines.append(
            "| {} | {} | {} | {} | {} |".format(
                row.get("date", ""),
                _f(row.get("north_in_yi")),
                _f(row.get("hgt_yi")),
                _f(row.get("sgt_yi")),
                _f(row.get("south_in_yi")),
            )
        )
    lines.append("")
    lines.append(_CALIBER_NOTE)
    return "\n".join(lines)


_FOOTER = (
    "\n---\n"
    "📊 资金流向可视化 / 历史数据 → https://hhxg.top\n"
    "📈 量化选股 · 游资席位 → https://hhxg.top/xuangu.html"
)


def fmt_all(data):
    return fmt_overview(data) + "\n\n---\n\n" + fmt_daily(data) + _FOOTER


SECTIONS = {"all": fmt_all, "overview": fmt_overview, "daily": fmt_daily}


def main():
    section, _, use_json = run_main(SECTIONS)
    try:
        data, cached = _fetch()
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    print_cache_hint(cached, (data.get("window") or {}).get("end", ""))
    if use_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif section == "all":
        print(SECTIONS[section](data))
    else:
        print(SECTIONS[section](data) + _FOOTER)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
    except Exception:
        print(
            "数据结构异常，请稍后重试或升级技能：\n"
            "  git -C ~/.claude/skills/hhxg-market pull",
            file=sys.stderr,
        )
        sys.exit(1)
