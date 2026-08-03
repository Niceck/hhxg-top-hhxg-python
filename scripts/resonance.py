#!/usr/bin/env python3
"""共振信号 + 风险警报 — 跨数据源多重确认与 4 类风险预警。

Usage:
    python3 resonance.py           # 完整（共振信号 + 风险警报）
    python3 resonance.py signals   # 仅共振信号
    python3 resonance.py risk      # 仅风险警报
    python3 resonance.py --json    # JSON 原始输出（合并两数据源）

数据来源: https://hhxg.top
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import as_dicts, fetch_json, md_inline, print_cache_hint, run_main

_RISK_BUCKETS = (
    ("crash", "暴跌"),
    ("distribution", "巨量出货"),
    ("nineturn_top_warning", "九转见顶"),
    ("high_turnover_drop", "高换手放量下跌"),
)

_CATEGORY_LABELS = {
    "hotmoney": "龙虎榜",
    "strategy": "策略",
    "theme": "题材",
    "indicator": "指标",
    "northbound": "北向",
}


def _fetch_signals():
    return fetch_json("assistant/resonance_latest.json", "resonance_latest.json")


def _fetch_risk():
    return fetch_json(
        "assistant/recent_risk_alerts_latest.json", "risk_alerts_latest.json"
    )


def _f(v, fmt="{:.2f}"):
    if v is None:
        return "—"
    try:
        return fmt.format(float(v))
    except (TypeError, ValueError):
        return str(v)


# ── Formatters ──────────────────────────────────────────────


def fmt_signals(data):
    stats = data.get("stats") or {}
    lines = [
        "# 跨数据源共振信号",
        "",
        "数据日期: {}".format(data.get("data_date", "?")),
        "信号数: {}（三重以上共振 {} 个）".format(
            stats.get("total", 0), stats.get("triple_plus", 0)
        ),
        "按数据源分布: "
        + " / ".join(
            f"{_CATEGORY_LABELS.get(k, k)} {v}"
            for k, v in (stats.get("by_category") or {}).items()
        ),
        "",
    ]
    missing = data.get("stats", {}) and (data.get("stats") or {}).get("missing_sources")
    if missing:
        lines.append(
            "⚠️ 数据源缺失: {}（共振信号可能少报）".format(
                "、".join(str(m) for m in missing)
            )
        )
        lines.append("")
    signals = as_dicts(data.get("signals"))
    if not signals:
        lines.append("今日无 ≥2 类数据源共振的个股。")
        return "\n".join(lines)

    for s in signals:
        cats = " + ".join(
            _CATEGORY_LABELS.get(c, c) for c in (s.get("categories") or [])
        )
        lines.append(
            "## {} ({}) — {}重共振 · 评分 {}".format(
                md_inline(s.get("name")),
                md_inline(s.get("code")),
                s.get("category_count", "?"),
                _f(s.get("score"), "{:.1f}"),
            )
        )
        if s.get("industry"):
            lines.append("行业: {}".format(md_inline(s.get("industry"))))
        lines.append(f"命中: {cats}")
        for d in s.get("details") or []:
            lines.append(f"- {md_inline(d)}")
        for w in s.get("warnings") or []:
            lines.append(f"- ⚠️ {md_inline(w)}")
        lines.append("")
    return "\n".join(lines).rstrip()


def fmt_risk(data):
    stats = data.get("stats") or {}
    # counts 是 top_n 截断后的榜单长度，total_counts 才是全市场命中数
    # （risk_alerts_builder 口径注释：正文引用必须用 total_counts）
    totals = stats.get("total_counts") or stats.get("counts") or {}
    lines = [
        "# 风险警报（4 类预警）",
        "",
        "覆盖全市场 {} 只，各类预警: ".format(stats.get("total_universe", "?"))
        + " / ".join(f"{label} {totals.get(key, 0)}" for key, label in _RISK_BUCKETS),
        "",
    ]
    alerts = data.get("alerts") or {}
    for key, label in _RISK_BUCKETS:
        rows = as_dicts(alerts.get(key))
        if not rows:
            continue
        total = totals.get(key, len(rows))
        lines.append(f"## {label}（全市场 {total} 只）")
        lines.append("| 股票 | 行业 | 涨跌% | 换手% | 量比 | 成交(亿) |")
        lines.append("|------|------|-------|-------|------|---------|")
        for r in rows[:5]:
            lines.append(
                "| {} | {} | {} | {} | {} | {} |".format(
                    md_inline(r.get("name")),
                    md_inline(r.get("industry")),
                    _f(r.get("pct")),
                    _f(r.get("turnover")),
                    _f(r.get("vol_ratio")),
                    _f(r.get("amount_yi")),
                )
            )
        if total > 5:
            lines.append(
                f"（仅列前 5，全市场共 {total} 只，榜单收录前 {stats.get('top_n', len(rows))}）"
            )
        lines.append("")
    return "\n".join(lines).rstrip()


_FOOTER = (
    "\n---\n"
    "⚠️ 风险提示：以上为量化信号提示，不构成投资建议。\n"
    "📊 完整信号与可视化 → https://hhxg.top\n"
    "📈 量化选股 · 策略回溯 → https://hhxg.top/xuangu.html"
)


SECTIONS = {"all": None, "signals": None, "risk": None}


def main():
    section, _, use_json = run_main(SECTIONS)

    res_data = risk_data = None
    try:
        if section in ("all", "signals"):
            res_data, res_cached = _fetch_signals()
            print_cache_hint(res_cached, res_data.get("data_date", ""))
        if section in ("all", "risk"):
            risk_data, risk_cached = _fetch_risk()
            print_cache_hint(risk_cached, str(risk_data.get("generated_at", ""))[:10])
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    if use_json:
        # 契约：单数据源 section 输出该源原始 JSON；all 输出命名 envelope
        if section == "signals":
            payload = res_data
        elif section == "risk":
            payload = risk_data
        else:
            payload = {"resonance": res_data, "risk_alerts": risk_data}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    parts = []
    if res_data is not None:
        parts.append(fmt_signals(res_data))
    if risk_data is not None:
        parts.append(fmt_risk(risk_data))
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
