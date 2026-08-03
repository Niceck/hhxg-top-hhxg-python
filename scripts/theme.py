#!/usr/bin/env python3
"""题材热点 — 题材热度排名 + 概念链路传导 + 龙头映射 + 共现关联。

Usage:
    python3 theme.py                    # 综合：热度榜 + 概念链龙头
    python3 theme.py ranking            # 仅题材热度排名（TOP 30）
    python3 theme.py chain              # 仅概念链路（龙头映射 + 传导）
    python3 theme.py related <概念名>    # 与某概念共现的相关概念
    python3 theme.py --json             # JSON 原始输出

数据来源: https://hhxg.top
- assistant/recent_theme_latest.json   — 当日题材热度排名
- assistant/concept_chain_latest.json  — 近 30 日涨停共现链路
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import as_dicts, fetch_json, md_inline, print_cache_hint, run_main


def _fetch_ranking():
    return fetch_json("assistant/recent_theme_latest.json", "theme_latest.json")


def _fetch_chain():
    return fetch_json("assistant/concept_chain_latest.json", "concept_chain.json")


def _num(v, fmt="{:.0f}"):
    if v is None:
        return "—"
    try:
        return fmt.format(float(v))
    except (TypeError, ValueError):
        return str(v)


def _pct(v):
    if v is None:
        return "—"
    try:
        return f"{float(v) * 100:.1f}%"
    except (TypeError, ValueError):
        return str(v)


# ── Formatters：当日热度榜 ──────────────────────────────────


def fmt_ranking(data, limit=30):
    items = as_dicts(data.get("items"))
    lines = [
        f"# 题材概念热度榜（TOP {min(limit, len(items))}）",
        "",
        "数据日期: {}".format(data.get("latest_date", "?")),
        "",
    ]
    if not items:
        lines.append("暂无题材数据")
        return "\n".join(lines)

    lines.append("| 排名 | 题材 | 游资参与数 | 当日涨停 | 涨停占比 |")
    lines.append("|------|------|-----------|---------|---------|")
    for i, it in enumerate(items[:limit], 1):
        lines.append(
            "| {} | {} | {} | {} | {} |".format(
                i,
                md_inline(it.get("name")),
                _num(it.get("yz")),
                _num(it.get("zt")),
                _pct(it.get("ratio")),
            )
        )
    return "\n".join(lines)


# ── Formatters：概念链路（近 30 日） ─────────────────────────


def fmt_chain(data):
    stats = data.get("stats") or {}
    top = data.get("top") or {}
    lines = [
        "# 题材概念链路（近 {} 日）".format(stats.get("window_days", 30)),
        "",
        "覆盖概念 {} 个 · 龙头股 {} 只 · 关联行业 {} 个".format(
            stats.get("total_concepts", "?"),
            stats.get("total_leaders", "?"),
            stats.get("total_industries", "?"),
        ),
        "",
    ]

    # 上游共现矩阵偶含 NaN 概念名（清洗遗漏），展示层过滤
    concepts = [
        c
        for c in as_dicts(top.get("concepts"))
        if str(c.get("name", "")).strip().lower() not in ("", "nan", "none")
    ]
    if concepts:
        lines.append("## TOP 热度概念")
        lines.append("| 排名 | 概念 | 累计涨停 | 活跃天数 | 最高连板 |")
        lines.append("|------|------|---------|---------|---------|")
        for i, c in enumerate(concepts[:12], 1):
            lines.append(
                "| {} | {} | {} | {} | {} |".format(
                    i,
                    md_inline(c.get("name")),
                    c.get("limitup_total", "—"),
                    c.get("active_days", "—"),
                    c.get("max_lianban", "—"),
                )
            )
        lines.append("")

    leaders = as_dicts(top.get("leaders"))
    if leaders:
        lines.append("## TOP 龙头股")
        lines.append("| 排名 | 股票 | 行业 | 涨停天数 | 最高连板 | 强度分 |")
        lines.append("|------|------|------|---------|---------|-------|")
        for i, ld in enumerate(leaders[:12], 1):
            lines.append(
                "| {} | {} | {} | {} | {} | {} |".format(
                    i,
                    md_inline(ld.get("name")),
                    md_inline(ld.get("industry") or "—"),
                    ld.get("limitup_days", "—"),
                    ld.get("max_lianban", "—"),
                    ld.get("score", "—"),
                )
            )
        lines.append("")

    mapping = top.get("concept_to_leaders") or {}
    if mapping:
        lines.append("## 概念 → 龙头映射（前 6 个概念）")
        for concept, stocks in list(mapping.items())[:6]:
            names = [
                md_inline(s.get("name")) if isinstance(s, dict) else md_inline(s)
                for s in (stocks[:5] if isinstance(stocks, list) else [])
            ]
            lines.append(
                "- **{}**: {}".format(
                    md_inline(concept), "、".join(n for n in names if n)
                )
            )
    return "\n".join(lines).rstrip()


def fmt_related(data, concept):
    related = data.get("related") or {}
    rel = related.get(concept)
    if not rel:
        hint = "、".join(list(related.keys())[:10])
        return (
            f"未找到概念「{concept}」的共现数据。\n"
            f"可查概念示例: {hint} …\n"
            "完整概念链 → https://hhxg.top"
        )
    lines = [f"# 与「{concept}」共现的相关概念", ""]
    for i, r in enumerate(as_dicts(rel)[:10], 1):
        lines.append(
            "{}. {}（共现 {} 次）".format(
                i, md_inline(r.get("name")), r.get("count", "?")
            )
        )
    return "\n".join(lines)


_FOOTER = (
    "\n---\n"
    "🔥 题材链传导可视化 / 概念成分股 → https://hhxg.top\n"
    "📈 量化选股 · 连板天梯 → https://hhxg.top/xuangu.html"
)


SECTIONS = {"all": None, "ranking": None, "chain": None, "related": None}


def main():
    section, rest, use_json = run_main(SECTIONS)

    if section == "related":
        if not rest:
            print("用法: python3 theme.py related <概念名>", file=sys.stderr)
            sys.exit(1)
        try:
            data, cached = _fetch_chain()
        except RuntimeError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
        print_cache_hint(cached, str(data.get("generated_at", ""))[:10])
        if use_json:
            payload = {
                "concept": rest[0],
                "related": data.get("related", {}).get(rest[0]),
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(fmt_related(data, rest[0]) + _FOOTER)
        return

    rank_data = chain_data = None
    try:
        if section in ("all", "ranking"):
            rank_data, cached = _fetch_ranking()
            print_cache_hint(cached, rank_data.get("latest_date", ""))
        if section in ("all", "chain"):
            chain_data, chain_cached = _fetch_chain()
            print_cache_hint(chain_cached, str(chain_data.get("generated_at", ""))[:10])
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    if use_json:
        if section == "ranking":
            print(json.dumps(rank_data, ensure_ascii=False, indent=2))
        elif section == "chain":
            print(json.dumps(chain_data, ensure_ascii=False, indent=2))
        else:
            print(
                json.dumps(
                    {"ranking": rank_data, "chain": chain_data},
                    ensure_ascii=False,
                    indent=2,
                )
            )
        return

    parts = []
    if rank_data is not None:
        parts.append(fmt_ranking(rank_data, 30))
    if chain_data is not None:
        parts.append(fmt_chain(chain_data))
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
