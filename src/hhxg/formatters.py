"""Human-readable formatters for AI tool output.

Each function takes a typed model and returns a markdown string
optimized for LLM consumption.
"""

from __future__ import annotations

from .models import (
    Hotmoney,
    LadderDetail,
    Market,
    HotTheme,
    NewsItem,
    SectorGroup,
    Snapshot,
)


def format_snapshot(snap: Snapshot) -> str:
    """Format the full snapshot as a concise AI-readable summary."""
    parts = [f"# A 股日报快照 — {snap.date or '未知日期'}"]
    parts.append(f"\n> {snap.disclaimer}")

    s = snap.ai_summary
    parts.append(f"\n## 市场概况\n- {s.market_state}")
    parts.append(f"- {s.focus_direction}")
    parts.append(f"- {s.theme_focus}")
    parts.append(f"- {s.hotmoney_state}")
    parts.append(f"- {s.news_highlight}")

    if snap.market:
        parts.append(f"\n{format_market(snap.market)}")
    if snap.hot_themes:
        parts.append(f"\n{format_hot_themes(snap.hot_themes)}")
    if snap.sectors:
        parts.append(f"\n{format_sectors(snap.sectors)}")
    if snap.ladder_detail:
        parts.append(f"\n{format_ladder(snap.ladder_detail)}")
    if snap.hotmoney:
        parts.append(f"\n{format_hotmoney(snap.hotmoney)}")
    if snap.focus_news:
        parts.append(f"\n{format_news(snap.focus_news)}")

    parts.append(f"\n---\n数据来源: [恢恢量化](https://hhxg.top)")
    return "\n".join(parts)


def format_market(m: Market) -> str:
    """Format market overview."""
    lines = [
        "## 市场赚钱效应",
        f"- 日期: {m.date}",
        f"- 赚钱效应: {m.sentiment_index}% ({m.sentiment_label})",
    ]
    if m.total:
        lines.append(f"- 个股总数: {m.total}")
    if m.struct_diff is not None:
        lines.append(f"- 结构差值: {m.struct_diff}")
    if m.limit_up is not None:
        lines.append(f"- 涨停: {m.limit_up}  炸板: {m.fried}  跌停: {m.limit_down}")
    if m.promotion_rate:
        lines.append(f"- 晋级率: {m.promotion_rate}")

    if m.buckets:
        lines.append("\n| 分类 | 今日 | 昨日 | 方向 |")
        lines.append("|------|------|------|------|")
        for b in m.buckets:
            lines.append(f"| {b.name} | {b.count} | {b.prev} | {b.dir} |")

    return "\n".join(lines)


def format_hot_themes(themes: list[HotTheme]) -> str:
    """Format hot themes table."""
    lines = [
        "## 热门题材",
        "| 题材 | 涨停数 | 净流入(亿) | 龙头股 |",
        "|------|--------|-----------|--------|",
    ]
    for t in themes:
        leaders = ", ".join(s.name for s in t.top_stocks[:2])
        net = f"{t.net_yi:.2f}" if t.net_yi is not None else "-"
        lines.append(f"| {t.name} | {t.limitup_count} | {net} | {leaders} |")
    return "\n".join(lines)


def format_sectors(groups: list[SectorGroup]) -> str:
    """Format sector fund-flow data."""
    lines = ["## 行业/板块资金流向"]
    for g in groups:
        lines.append(f"\n### {g.label}")
        if g.strong:
            lines.append("\n**强势:**")
            lines.append("| 名称 | 净流入(亿) | 领涨 | 偏离% |")
            lines.append("|------|-----------|------|-------|")
            for s in g.strong:
                net = f"{s.net_yi:.1f}" if s.net_yi is not None else "-"
                bias = f"{s.bias_pct:.1f}" if s.bias_pct is not None else "-"
                lines.append(f"| {s.name} | {net} | {s.leader or '-'} | {bias} |")
        if g.weak:
            lines.append("\n**弱势:**")
            lines.append("| 名称 | 净流入(亿) | 领涨 | 偏离% |")
            lines.append("|------|-----------|------|-------|")
            for s in g.weak:
                net = f"{s.net_yi:.1f}" if s.net_yi is not None else "-"
                bias = f"{s.bias_pct:.1f}" if s.bias_pct is not None else "-"
                lines.append(f"| {s.name} | {net} | {s.leader or '-'} | {bias} |")
    return "\n".join(lines)


def format_ladder(detail: LadderDetail) -> str:
    """Format the consecutive limit-up ladder."""
    lines = ["## 连板天梯"]

    if detail.lb_rates_map:
        rates = ", ".join(f"{k}板→{v}" for k, v in sorted(detail.lb_rates_map.items()))
        lines.append(f"晋级率: {rates}")

    for level in detail.levels:
        names = ", ".join(
            f"{s.name}({s.code})" if s.code else s.name
            for s in level.stocks[:5]
        )
        suffix = f" +{level.count - 5}只" if level.count > 5 else ""
        lines.append(f"- **{level.boards}板** ({level.count}只): {names}{suffix}")

    if detail.area_counts:
        top_areas = sorted(detail.area_counts.items(), key=lambda x: -x[1])[:5]
        lines.append(f"\n地域分布: {', '.join(f'{k}({v})' for k, v in top_areas)}")
    if detail.concept_counts:
        top_concepts = sorted(detail.concept_counts.items(), key=lambda x: -x[1])[:5]
        lines.append(f"概念分布: {', '.join(f'{k}({v})' for k, v in top_concepts)}")

    return "\n".join(lines)


def format_hotmoney(hm: Hotmoney) -> str:
    """Format hotmoney / Dragon-Tiger board data."""
    lines = [
        "## 游资龙虎榜",
        f"- 日期: {hm.date}",
    ]
    if hm.total_net_yi is not None:
        lines.append(f"- 合计净买入: {hm.total_net_yi:.2f} 亿")

    if hm.top_net_buy:
        lines.append("\n**净买入 TOP:**")
        lines.append("| 股票 | 净买入(亿) | 占比% |")
        lines.append("|------|-----------|-------|")
        for b in hm.top_net_buy:
            ratio = f"{b.ratio_pct:.1f}" if b.ratio_pct is not None else "-"
            lines.append(f"| {b.name} | {b.net_yi:.2f} | {ratio} |")

    if hm.seats:
        lines.append("\n**知名游资席位:**")
        for seat in hm.seats:
            stocks_str = ", ".join(
                f"{s.name}({'+' if s.net_yi >= 0 else ''}{s.net_yi:.2f}亿)"
                for s in seat.stocks[:5]
            )
            lines.append(f"- **{seat.name}**: {stocks_str}")

    return "\n".join(lines)


def format_news(items: list[NewsItem]) -> str:
    """Format news items."""
    lines = ["## 焦点新闻"]
    for n in items:
        lines.append(f"- [{n.cat}] {n.title}")
    return "\n".join(lines)
