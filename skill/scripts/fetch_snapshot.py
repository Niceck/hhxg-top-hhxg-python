#!/usr/bin/env python3
"""A 股日报快照获取脚本 — 零依赖，仅需 Python 3 标准库。

Usage:
    python3 fetch_snapshot.py          # 完整快照
    python3 fetch_snapshot.py market   # 市场赚钱效应
    python3 fetch_snapshot.py themes   # 热门题材
    python3 fetch_snapshot.py ladder   # 连板天梯
    python3 fetch_snapshot.py hotmoney # 游资龙虎榜
    python3 fetch_snapshot.py sectors  # 行业资金
    python3 fetch_snapshot.py news     # 焦点新闻

数据来源: https://hhxg.top
"""

from __future__ import annotations

import json
import sys
import urllib.request

URL = "https://hhxg.top/static/data/assistant/skill_snapshot.json"


def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": "hhxg-skill/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ── Formatters ──────────────────────────────────────────────


def fmt_market(data):
    m = data.get("market")
    if not m:
        return "暂无市场数据"
    lines = [
        "# 市场赚钱效应 — %s" % data.get("date", ""),
        "",
        "赚钱效应指数: **%s%%** (%s)" % (m.get("sentiment_index", "?"), m.get("sentiment_label", "?")),
        "涨停 %s | 炸板 %s | 跌停 %s" % (m.get("limit_up", "?"), m.get("fried", "?"), m.get("limit_down", "?")),
        "结构差值: %s  |  晋级率: %s" % (m.get("struct_diff", "?"), m.get("promotion_rate", "?")),
        "",
        "### 涨跌分布",
        "| 区间 | 数量 |",
        "|------|------|",
    ]
    for b in m.get("buckets", []):
        lines.append("| %s | %s |" % (b.get("name", "?"), b.get("count", "?")))
    return "\n".join(lines)


def fmt_themes(data):
    themes = data.get("hot_themes", [])
    if not themes:
        return "暂无热门题材数据"
    lines = [
        "# 热门题材 — %s" % data.get("date", ""),
        "",
        "| # | 题材 | 涨停数 | 净流入(亿) | 龙头股 |",
        "|---|------|--------|-----------|--------|",
    ]
    for i, t in enumerate(themes, 1):
        leaders = ", ".join(s.get("name", "") for s in t.get("top_stocks", [])[:3])
        net = t.get("net_yi", "-")
        lines.append("| %d | %s | %s | %s | %s |" % (i, t.get("name", ""), t.get("limitup_count", ""), net, leaders))
    return "\n".join(lines)


def fmt_ladder(data):
    ld = data.get("ladder_detail")
    if not ld:
        return "暂无连板数据"
    ladder = data.get("ladder", {})
    ts = ladder.get("top_streak", {})
    lines = [
        "# 连板天梯 — %s" % data.get("date", ""),
        "",
        "最高连板: **%s板** — %s (%s)" % (
            ladder.get("max_streak", "?"),
            ts.get("name", "?"),
            ts.get("industry", ""),
        ),
        "涨停总数: %s" % ladder.get("total_limit_up", "?"),
        "",
    ]
    for level in ld.get("levels", []):
        boards = level.get("boards", "?")
        stocks = level.get("stocks", [])
        names = " / ".join(
            "%s(%s)" % (s.get("name", ""), s.get("code", "")) for s in stocks[:8]
        )
        lines.append("### %s板（%s 只）" % (boards, level.get("count", len(stocks))))
        lines.append(names)
        lines.append("")

    rates = ld.get("lb_rates_map", {})
    if rates:
        lines.append("### 晋级率")
        for k, v in rates.items():
            lines.append("- %s: %s" % (k, v))

    areas = ld.get("area_counts", {})
    if areas:
        lines.append("")
        lines.append("### 地域分布 TOP 5")
        for name, count in list(areas.items())[:5]:
            lines.append("- %s: %s 只" % (name, count))

    concepts = ld.get("concept_counts", {})
    if concepts:
        lines.append("")
        lines.append("### 概念分布 TOP 5")
        for name, count in list(concepts.items())[:5]:
            lines.append("- %s: %s 只" % (name, count))

    return "\n".join(lines)


def fmt_hotmoney(data):
    hm = data.get("hotmoney")
    if not hm:
        return "暂无游资数据"
    lines = [
        "# 游资龙虎榜 — %s" % data.get("date", ""),
        "",
        "龙虎榜总净买入: %s 亿" % hm.get("total_net_yi", "?"),
        "",
        "### 净买入 TOP",
        "| 股票 | 净买入(亿) | 占比 |",
        "|------|-----------|------|",
    ]
    for b in hm.get("top_net_buy", [])[:10]:
        lines.append("| %s | %s | %s%% |" % (
            b.get("name", "-"), b.get("net_yi", "-"), b.get("ratio_pct", "-"),
        ))

    seats = hm.get("seats", [])
    if seats:
        lines.append("")
        lines.append("### 知名游资席位")
        for seat in seats[:10]:
            stocks_str = ", ".join(
                "%s(%s亿)" % (st.get("name", ""), st.get("net_yi", ""))
                for st in seat.get("stocks", [])[:5]
            )
            lines.append("- **%s**: %s" % (seat.get("name", ""), stocks_str))

    return "\n".join(lines)


def fmt_sectors(data):
    sectors = data.get("sectors", [])
    if not sectors:
        return "暂无行业资金数据"
    lines = ["# 行业资金流向 — %s" % data.get("date", "")]
    for group in sectors:
        label = group.get("label", "")
        lines.append("\n## %s" % label)
        for section_key in ("strong", "weak"):
            section = group.get(section_key, [])
            if not section:
                continue
            tag = "强势" if section_key == "strong" else "弱势"
            lines.append("\n### %s" % tag)
            lines.append("| 板块 | 净流入(亿) | 领涨股 | 偏离度 |")
            lines.append("|------|-----------|--------|--------|")
            for item in section[:8]:
                lines.append("| %s | %s | %s | %s%% |" % (
                    item.get("name", "-"),
                    item.get("net_yi", "-"),
                    item.get("leader", "-"),
                    item.get("bias_pct", "-"),
                ))
    return "\n".join(lines)


def fmt_news(data):
    focus = data.get("focus_news", [])
    macro = data.get("macro_news", [])
    if not focus and not macro:
        return "暂无新闻数据"
    lines = ["# 焦点新闻 — %s" % data.get("date", "")]
    if focus:
        lines.append("\n## 市场焦点")
        for n in focus:
            t = n.get("t", "")
            if "T" in t:
                t = t.split("T")[1][:5]
            lines.append("- [%s] %s" % (t, n.get("title", "")))
    if macro:
        lines.append("\n## 宏观新闻")
        for n in macro:
            t = n.get("t", "")
            if "T" in t:
                t = t.split("T")[1][:5]
            lines.append("- [%s] %s" % (t, n.get("title", "")))
    return "\n".join(lines)


def fmt_snapshot(data):
    """完整快照"""
    parts = [
        "# A 股日报快照 — %s" % data.get("date", ""),
        "",
    ]
    ai = data.get("ai_summary", {})
    if isinstance(ai, dict) and ai.get("one_line"):
        parts.append("> %s" % ai["one_line"])
        parts.append("")
    elif isinstance(ai, str) and ai:
        parts.append("> %s" % ai)
        parts.append("")

    sep = "\n\n---\n\n"
    parts.append(fmt_market(data))
    parts.append(sep)
    parts.append(fmt_themes(data))
    parts.append(sep)
    parts.append(fmt_ladder(data))
    parts.append(sep)
    parts.append(fmt_hotmoney(data))
    parts.append(sep)
    parts.append(fmt_sectors(data))
    parts.append(sep)
    parts.append(fmt_news(data))
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("数据来源: 恢恢量化 https://hhxg.top")
    return "\n".join(parts)


# ── Main ────────────────────────────────────────────────────

SECTIONS = {
    "all": fmt_snapshot,
    "market": fmt_market,
    "themes": fmt_themes,
    "ladder": fmt_ladder,
    "hotmoney": fmt_hotmoney,
    "sectors": fmt_sectors,
    "news": fmt_news,
}


def main():
    section = sys.argv[1] if len(sys.argv) > 1 else "all"
    if section not in SECTIONS:
        print("未知板块: %s" % section)
        print("可选: %s" % ", ".join(SECTIONS))
        sys.exit(1)

    try:
        data = fetch()
    except Exception as e:
        print("获取数据失败: %s" % e)
        sys.exit(1)

    print(SECTIONS[section](data))


if __name__ == "__main__":
    main()
