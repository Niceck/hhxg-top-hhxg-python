#!/usr/bin/env python3
"""量化策略选股 — 策略审计、最新信号、历史胜率、游资席位。

Usage:
    python3 strategy.py           # 概览（审计 + 席位 + 胜率摘要）
    python3 strategy.py presets   # 全部策略审计结果（当日命中）
    python3 strategy.py signals   # 最新信号（待开仓/持仓/清仓）
    python3 strategy.py stats     # 历史全量统计（胜率/分布/月度）
    python3 strategy.py seats     # 游资席位持仓
    python3 strategy.py --json    # JSON 原始输出

数据来源: https://hhxg.top
- xuangu/preset_audit.json               — 14 个预设策略审计
- assistant/recent_strategy_latest.json  — 最新策略信号
- assistant/strategy_full_stats.json     — 历史胜率统计
- xuangu/hotmoney_seats.json             — 游资席位 → 持仓映射
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import as_dicts, fetch_json, md_inline, print_cache_hint, run_main


def _fetch_audit():
    return fetch_json("xuangu/preset_audit.json", "preset_audit.json")


def _fetch_signals():
    return fetch_json("assistant/recent_strategy_latest.json", "strategy_latest.json")


def _fetch_stats():
    return fetch_json("assistant/strategy_full_stats.json", "strategy_stats.json")


def _fetch_seats():
    return fetch_json("xuangu/hotmoney_seats.json", "hotmoney_seats.json")


def _f(v, fmt="{:.2f}"):
    if v is None:
        return "—"
    try:
        return fmt.format(float(v))
    except (TypeError, ValueError):
        return str(v)


# ── Formatters ──────────────────────────────────────────────


_COVERAGE_LABELS = {
    "pass": "覆盖达标",
    "fail_undershoot": "命中过少",
    "fail_overshoot": "命中过多",
    "fail_zero": "零命中",
}


def fmt_presets(data):
    summary = data.get("summary") or {}
    lines = [
        "# 策略审计（{}）".format(data.get("asof_used", "?")),
        "",
        "策略总数 {} · 覆盖达标 {} · 未达标 {} · 选股宇宙 {} 只".format(
            summary.get("preset_total", "?"),
            summary.get("coverage_pass", "?"),
            summary.get("coverage_fail", "?"),
            data.get("universe_size", "?"),
        ),
        "",
        "| 策略 | 阶段 | 覆盖率检查 | 胜率 | 今日命中 |",
        "|------|------|-----------|------|---------|",
    ]
    for p in as_dicts(data.get("presets")):
        label = md_inline(p.get("label") or p.get("key") or "")
        stage = md_inline(p.get("strategy_status_label") or "—")
        check = p.get("coverage_check")
        coverage = _COVERAGE_LABELS.get(check, str(check or "—"))
        metrics = ((p.get("quality") or {}).get("metrics")) or {}
        win_rate = _f(metrics.get("win_rate_pct"), "{:.1f}")
        win_cell = f"{win_rate}%" if win_rate != "—" else "—"
        lines.append(
            f"| {label} | {stage} | {coverage} | {win_cell} "
            f"| {_f(p.get('asof_hits'), '{:.0f}')} 只 |"
        )

    # 治理免责：覆盖率检查 ≠ 策略有效性背书（governance.status_semantics）
    note = (((data.get("governance") or {}).get("dev_sample")) or {}).get("note")
    lines.append("")
    lines.append("> 覆盖率检查仅衡量当日命中数是否落在目标区间，不构成策略有效性背书。")
    if note:
        lines.append(f"> {md_inline(note)}")
    return "\n".join(lines)


def fmt_signals(data):
    summary = data.get("summary") or {}
    lines = [
        "# 量化策略最新信号",
        "",
        "策略日期: {}".format(data.get("latest_strategy_date", "?")),
        "待开仓 {} / 持仓 {} / 已清仓 {}".format(
            summary.get("pending", 0),
            summary.get("holding", 0),
            summary.get("cleared", 0),
        ),
        "",
    ]
    pending = as_dicts(data.get("pending"))
    if pending:
        lines.append("## 待开仓")
        for p in pending:
            lines.append(
                "- {}（信号日 {}）".format(md_inline(p.get("name")), p.get("date", ""))
            )
        lines.append("")

    holding = as_dicts(data.get("holding_top"))
    if holding:
        lines.append("## 持仓盈亏 TOP")
        lines.append("| 股票 | 买入日 | 浮动盈亏% |")
        lines.append("|------|--------|----------|")
        for h in holding:
            lines.append(
                "| {} | {} | {} |".format(
                    md_inline(h.get("name")), h.get("buy_date", ""), _f(h.get("pnl"))
                )
            )
        lines.append("")

    cleared = as_dicts(data.get("cleared_recent"))
    if cleared:
        lines.append("## 近期清仓（前 10）")
        lines.append("| 股票 | 买入日 | 清仓日 | 收益% |")
        lines.append("|------|--------|--------|-------|")
        for c in cleared[:10]:
            lines.append(
                "| {} | {} | {} | {} |".format(
                    md_inline(c.get("name")),
                    c.get("buy_date", ""),
                    c.get("sell_date", ""),
                    _f(c.get("ret")),
                )
            )
    return "\n".join(lines).rstrip()


def fmt_stats(data):
    stats = data.get("stats") or {}
    recent = data.get("recent_30d") or {}
    lines = [
        "# 策略历史全量统计",
        "",
        "总交易 {} 笔：胜 {} / 负 {} / 平 {}，胜率 **{}**".format(
            stats.get("total", 0),
            stats.get("wins", 0),
            stats.get("losses", 0),
            stats.get("even", 0),
            stats.get("win_rate", "?"),
        ),
        "平均收益 {}% · 中位数 {}% · 最大 {}% · 最小 {}%".format(
            _f(stats.get("avg_return")),
            _f(stats.get("median_return")),
            _f(stats.get("max_return")),
            _f(stats.get("min_return")),
        ),
        "近 30 日: {} 笔 · 胜率 {} · 均值 {}%".format(
            recent.get("笔数", "?"), recent.get("胜率", "?"), _f(recent.get("均值"))
        ),
        "",
    ]

    dist = data.get("distribution") or {}
    if dist:
        lines.append("## 收益分布")
        lines.append("| 区间 | 笔数 |")
        lines.append("|------|------|")
        for bucket, cnt in dist.items():
            lines.append(f"| {bucket} | {cnt} |")
        lines.append("")

    monthly = as_dicts(data.get("monthly"))
    if monthly:
        lines.append("## 月度表现（近 6 个月）")
        lines.append("| 月份 | 笔数 | 均值% | 胜率 |")
        lines.append("|------|------|-------|------|")
        for m in monthly[-6:]:
            lines.append(
                "| {} | {} | {} | {} |".format(
                    m.get("月份", ""),
                    m.get("笔数", ""),
                    _f(m.get("均值")),
                    m.get("胜率", ""),
                )
            )
        lines.append("")

    winners = as_dicts(data.get("top_winners"))
    if winners:
        lines.append("## 历史最佳（前 3）")
        for w in winners[:3]:
            lines.append(
                "- {}：{}%（{} → {}）".format(
                    md_inline(w.get("股票名称")),
                    w.get("保底收益", "?"),
                    w.get("买入日期", ""),
                    w.get("清仓日期", ""),
                )
            )
    losers = as_dicts(data.get("top_losers"))
    if losers:
        lines.append("")
        lines.append("## 历史最差（前 3）")
        for w in losers[:3]:
            lines.append(
                "- {}：{}%（{} → {}）".format(
                    md_inline(w.get("股票名称")),
                    w.get("保底收益", "?"),
                    w.get("买入日期", ""),
                    w.get("清仓日期", ""),
                )
            )
    return "\n".join(lines).rstrip()


def fmt_seats(data, limit=None):
    seats = {k: v for k, v in (data or {}).items() if isinstance(v, list) and v}
    if not seats:
        return "暂无游资席位数据"
    lines = ["# 游资席位持仓一览", ""]
    ranked = sorted(seats.items(), key=lambda x: -len(x[1]))
    if limit:
        ranked = ranked[:limit]
    for name, codes in ranked:
        preview = ", ".join(str(c) for c in codes[:8])
        if len(codes) > 8:
            preview += f" …共{len(codes)}只"
        lines.append(f"- **{md_inline(name)}**（{len(codes)}只）: {preview}")
    return "\n".join(lines)


_FOOTER = (
    "\n---\n"
    "⚠️ 风险提示：历史表现不代表未来收益，不构成投资建议。\n"
    "📈 策略明细 · 回测 · 选股工具 → https://hhxg.top/xuangu.html"
)


SECTIONS = {
    "all": None,
    "presets": None,
    "signals": None,
    "stats": None,
    "seats": None,
}

# section → (数据键, fetch 函数, 格式化函数)
_FETCHERS = {
    "presets": ("audit", _fetch_audit, fmt_presets),
    "signals": ("signals", _fetch_signals, fmt_signals),
    "stats": ("stats", _fetch_stats, fmt_stats),
    "seats": ("seats", _fetch_seats, fmt_seats),
}
# all 概览：审计 + 席位前 10 + 胜率摘要
_ALL_PARTS = ("presets", "seats", "stats")


def main():
    section, _, use_json = run_main(SECTIONS)
    wanted = _ALL_PARTS if section == "all" else (section,)

    fetched = {}
    hint_keys = {
        "presets": "asof_used",
        "signals": "latest_strategy_date",
        "stats": "generated_at",
        "seats": None,
    }
    try:
        for part in wanted:
            key, fetch, _fmt = _FETCHERS[part]
            data, cached = fetch()
            fetched[part] = data
            hk = hint_keys.get(part)
            hint = str(data.get(hk, ""))[:10] if hk and isinstance(data, dict) else ""
            print_cache_hint(cached, hint)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    if use_json:
        if section == "all":
            payload = {_FETCHERS[p][0]: fetched[p] for p in wanted}
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(fetched[section], ensure_ascii=False, indent=2))
        return

    parts = []
    for part in wanted:
        _key, _fetch, fmt = _FETCHERS[part]
        if section == "all" and part == "seats":
            parts.append(fmt_seats(fetched[part], limit=10))
        else:
            parts.append(fmt(fetched[part]))
    print("\n\n---\n\n".join(parts) + _FOOTER)


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
