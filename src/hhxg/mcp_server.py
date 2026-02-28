"""MCP (Model Context Protocol) server for hhxg.

Exposes A-share daily market data as MCP tools for Claude Desktop,
Cursor, Claude Code, and other MCP-compatible AI clients.

Usage:
    # stdio transport (default)
    hhxg-mcp

    # or via Python module
    python -m hhxg.mcp_server
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .client import HhxgClient
from .formatters import (
    format_hot_themes,
    format_hotmoney,
    format_ladder,
    format_market,
    format_news,
    format_sectors,
    format_snapshot,
)

mcp = FastMCP(
    "hhxg",
    instructions=(
        "A 股日报快照 — 零配置获取赚钱效应、"
        "热门题材、连板天梯、游资龙虎榜等实时数据"
    ),
)

_client = HhxgClient()


@mcp.tool()
def get_snapshot() -> str:
    """获取完整的 A 股日报快照。

    包含市场赚钱效应、热门题材、行业资金、连板天梯、游资龙虎榜、焦点新闻。
    这是最全面的工具，适合需要市场全貌时调用。数据每个交易日盘后更新。
    """
    snap = _client.get_snapshot(force=True)
    return format_snapshot(snap)


@mcp.tool()
def get_market() -> str:
    """获取 A 股市场赚钱效应指数。

    返回赚钱效应百分比、涨跌家数分布、涨停/炸板/跌停数、结构差值等。
    适合快速判断当日市场情绪强弱。
    """
    snap = _client.get_snapshot()
    if snap.market is None:
        return "暂无市场数据"
    return format_market(snap.market)


@mcp.tool()
def get_hot_themes() -> str:
    """获取当日热门题材/概念排行。

    返回涨停数最多的题材，包含龙头股和净流入金额。
    适合了解市场热点方向和主线题材。
    """
    snap = _client.get_snapshot()
    if not snap.hot_themes:
        return "暂无热门题材数据"
    return format_hot_themes(snap.hot_themes)


@mcp.tool()
def get_sectors() -> str:
    """获取行业/板块资金流向排行。

    返回资金净流入最强和最弱的行业及板块，包含领涨股和偏离度。
    适合分析资金流向和行业轮动。
    """
    snap = _client.get_snapshot()
    if not snap.sectors:
        return "暂无行业资金数据"
    return format_sectors(snap.sectors)


@mcp.tool()
def get_ladder() -> str:
    """获取连板天梯（连续涨停排行）。

    返回各级连板股票明细、晋级率、地域分布和概念分布。
    适合追踪市场高度和情绪龙头。
    """
    snap = _client.get_snapshot()
    if snap.ladder_detail is None:
        return "暂无连板数据"
    return format_ladder(snap.ladder_detail)


@mcp.tool()
def get_hotmoney() -> str:
    """获取游资龙虎榜数据。

    返回龙虎榜净买入 TOP 个股和知名游资席位（如赵老哥、炒股养家等）的操作明细。
    适合跟踪游资动向和市场主力资金。
    """
    snap = _client.get_snapshot()
    if snap.hotmoney is None:
        return "暂无游资数据"
    return format_hotmoney(snap.hotmoney)


@mcp.tool()
def get_news() -> str:
    """获取当日焦点新闻和宏观新闻。

    返回最重要的市场新闻，按时间倒序排列。
    适合快速了解影响市场的关键事件。
    """
    snap = _client.get_snapshot()
    items = snap.focus_news + snap.macro_news
    if not items:
        return "暂无新闻数据"
    return format_news(items)


def main() -> None:
    """Entry point for the hhxg MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
