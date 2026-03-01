#!/usr/bin/env python3
"""量化选股策略 — 策略审计、胜率排名。

Usage:
    python3 strategy.py           # 策略概览
    python3 strategy.py presets   # 所有策略审计结果
    python3 strategy.py seats     # 游资席位持仓
    python3 strategy.py --json    # JSON 原始输出

数据来源: https://hhxg.top
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import fetch_json, print_cache_hint, run_main


def _fetch_audit():
    return fetch_json("xuangu/preset_audit.json", "preset_audit.json")


def _fetch_seats():
    return fetch_json("xuangu/hotmoney_seats.json", "hotmoney_seats.json")


# ── Formatters ──────────────────────────────────────────────


def fmt_presets(data):
    summary = data.get("summary", {})
    presets = data.get("presets", [])
    asof = data.get("asof_used", "")
    lines = [
        "# 量化选股策略 — %s" % asof,
        "",
        "策略总数: %s | 达标: %s | 未达标: %s" % (
            summary.get("preset_total", "?"),
            summary.get("coverage_pass", "?"),
            summary.get("coverage_fail", "?"),
        ),
        "选股宇宙: %s 只" % data.get("universe_size", "?"),
        "",
        "| 策略 | 状态 | 今日命中 |",
        "|------|------|---------|",
    ]
    for p in presets:
        label = p.get("label", p.get("key", ""))
        status = "PASS" if p.get("coverage_check") == "pass" else "FAIL"
        count = p.get("asof_hits", "?")
        lines.append("| %s | %s | %s只 |" % (label, status, count))

    lines.append("")
    lines.append("完整回测数据（胜率/收益/持仓周期）→ https://hhxg.top/xuangu.html#backtest")

    return "\n".join(lines)


def fmt_seats(data):
    if not data:
        return "暂无游资席位数据"
    lines = ["# 游资席位持仓一览", ""]
    for name, codes in sorted(data.items(), key=lambda x: -len(x[1])):
        count = len(codes)
        preview = ", ".join(codes[:8])
        if count > 8:
            preview += " …共%d只" % count
        lines.append("- **%s**（%d只）: %s" % (name, count, preview))
    return "\n".join(lines)


def fmt_overview(data_audit, data_seats):
    lines = [fmt_presets(data_audit)]
    if data_seats:
        lines.append("\n\n---\n\n")
        # 仅展示前 10 个席位
        top_seats = dict(sorted(data_seats.items(), key=lambda x: -len(x[1]))[:10])
        lines.append(fmt_seats(top_seats))
    return "".join(lines)


SECTIONS = {"all": "all", "presets": "presets", "seats": "seats"}


def main():
    section, _, use_json = run_main(SECTIONS)

    data_audit = data_seats = None
    try:
        if section in ("all", "presets"):
            data_audit, cached1 = _fetch_audit()
            print_cache_hint(cached1, data_audit.get("asof_used", ""))
        if section in ("all", "seats"):
            data_seats, cached2 = _fetch_seats()
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    if use_json:
        if section == "presets":
            print(json.dumps(data_audit, ensure_ascii=False, indent=2))
        elif section == "seats":
            print(json.dumps(data_seats, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"audit": data_audit, "seats": data_seats}, ensure_ascii=False, indent=2))
        return

    if section == "presets":
        print(fmt_presets(data_audit))
    elif section == "seats":
        print(fmt_seats(data_seats))
    else:
        print(fmt_overview(data_audit, data_seats))


if __name__ == "__main__":
    main()
