"""hhxg — A-share daily market snapshot SDK.

Zero-config, type-safe access to Chinese A-share market data.

Quick start::

    import hhxg

    snapshot = hhxg.get_snapshot()
    print(snapshot.market.sentiment_index)
"""

from __future__ import annotations

from .client import HhxgClient
from .exceptions import HhxgError, NetworkError, SchemaError
from .models import (
    AISummary,
    Bucket,
    Hotmoney,
    HotmoneyBuy,
    HotmoneySeat,
    HotmoneyStock,
    HotTheme,
    Ladder,
    LadderDetail,
    LadderLevel,
    LadderStock,
    LadderTopStreak,
    Link,
    Market,
    NewsItem,
    SectorGroup,
    SectorItem,
    Snapshot,
    SnapshotMeta,
    TopStock,
)

__version__ = "0.1.0"

# Module-level shared client (lazy singleton)
_client: HhxgClient | None = None


def _get_client() -> HhxgClient:
    global _client  # noqa: PLW0603
    if _client is None:
        _client = HhxgClient()
    return _client


# ---- Convenience functions ----


def get_snapshot() -> Snapshot:
    """Fetch the complete daily market snapshot."""
    return _get_client().get_snapshot()


def get_market() -> Market | None:
    """Fetch market overview (sentiment, rise/fall distribution)."""
    return get_snapshot().market


def get_hot_themes() -> list[HotTheme]:
    """Fetch today's hot themes / concepts."""
    return get_snapshot().hot_themes


def get_sectors() -> list[SectorGroup]:
    """Fetch sector fund-flow data (industry + concept groups)."""
    return get_snapshot().sectors


def get_ladder() -> LadderDetail | None:
    """Fetch the consecutive limit-up ladder detail."""
    return get_snapshot().ladder_detail


def get_hotmoney() -> Hotmoney | None:
    """Fetch Dragon-Tiger board (hotmoney) data."""
    return get_snapshot().hotmoney


def get_news() -> list[NewsItem]:
    """Fetch focus news items."""
    return get_snapshot().focus_news


__all__ = [
    # convenience functions
    "get_snapshot",
    "get_market",
    "get_hot_themes",
    "get_sectors",
    "get_ladder",
    "get_hotmoney",
    "get_news",
    # client
    "HhxgClient",
    # models
    "AISummary",
    "Bucket",
    "Hotmoney",
    "HotmoneyBuy",
    "HotmoneySeat",
    "HotmoneyStock",
    "HotTheme",
    "Ladder",
    "LadderDetail",
    "LadderLevel",
    "LadderStock",
    "LadderTopStreak",
    "Link",
    "Market",
    "NewsItem",
    "SectorGroup",
    "SectorItem",
    "Snapshot",
    "SnapshotMeta",
    "TopStock",
    # exceptions
    "HhxgError",
    "NetworkError",
    "SchemaError",
    # formatters
    "formatters",
    # version
    "__version__",
]
