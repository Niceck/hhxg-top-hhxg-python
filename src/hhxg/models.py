"""Pydantic v2 models for hhxg skill_snapshot.json (schema v3).

All field names match the JSON keys exactly — no aliasing or mapping.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ---- Meta ----


class SnapshotMeta(BaseModel):
    """Snapshot metadata: provider info, update time, schema version."""

    provider: str
    provider_name: str
    update_time: str
    market: str
    language: str
    schema_version: int
    usage: str


# ---- AI Summary ----


class AISummary(BaseModel):
    """AI-friendly market state summary (descriptive, not investment advice)."""

    market_state: str
    focus_direction: str
    theme_focus: str
    hotmoney_state: str
    news_highlight: str
    cta: str


# ---- Market ----


class Bucket(BaseModel):
    """Rise/fall distribution bucket."""

    name: str
    count: int
    prev: int
    dir: str


class Market(BaseModel):
    """Market overview: sentiment, rise/fall distribution, limit-up/down."""

    date: str
    sentiment_index: float
    sentiment_label: str
    struct_diff: float | None = None
    total: int | None = None
    buckets: list[Bucket] = Field(default_factory=list)
    limit_up: int | None = None
    fried: int | None = None
    limit_down: int | None = None
    promotion_rate: str | None = None


# ---- Hot Themes ----


class TopStock(BaseModel):
    """Leading stock within a hot theme."""

    name: str
    net_yi: float | None = None


class HotTheme(BaseModel):
    """Hot theme / concept with limit-up count and leading stocks."""

    name: str
    limitup_count: int = 0
    net_yi: float | None = None
    top_stocks: list[TopStock] = Field(default_factory=list)


# ---- Sectors ----


class SectorItem(BaseModel):
    """Single sector/industry item with fund flow data."""

    name: str
    net_yi: float | None = None
    leader: str | None = None
    bias_pct: float | None = None


class SectorGroup(BaseModel):
    """Grouped sector data (e.g. by industry or concept)."""

    label: str
    strong: list[SectorItem] = Field(default_factory=list)
    weak: list[SectorItem] = Field(default_factory=list)


# ---- Ladder ----


class LadderTopStreak(BaseModel):
    """Top streak stock in the consecutive limit-up ladder."""

    name: str
    boards: int
    industry: str = ""


class Ladder(BaseModel):
    """Consecutive limit-up ladder summary."""

    total_limit_up: int | None = None
    max_streak: int | None = None
    top_streak: LadderTopStreak | None = None


class LadderStock(BaseModel):
    """Stock in a ladder level with full identification."""

    name: str
    code: str = ""
    industry: str = ""
    area: str = ""
    concept: str = ""


class LadderLevel(BaseModel):
    """A single level in the ladder (grouped by board count)."""

    boards: int
    count: int
    stocks: list[LadderStock] = Field(default_factory=list)


class LadderDetail(BaseModel):
    """Full ladder breakdown with levels, promotion rates, and distributions."""

    levels: list[LadderLevel] = Field(default_factory=list)
    lb_rates_map: dict[str, str] = Field(default_factory=dict)
    area_counts: dict[str, int] = Field(default_factory=dict)
    concept_counts: dict[str, int] = Field(default_factory=dict)


# ---- News ----


class NewsItem(BaseModel):
    """A single news item with timestamp and category."""

    t: str
    cat: str
    title: str


# ---- Hotmoney ----


class HotmoneyBuy(BaseModel):
    """Top net-buy stock on the Dragon-Tiger board."""

    name: str
    net_yi: float
    ratio_pct: float | None = None


class HotmoneyStock(BaseModel):
    """Stock traded by a known hotmoney seat."""

    name: str
    net_yi: float


class HotmoneySeat(BaseModel):
    """Known hotmoney seat (e.g. famous trader) and their trades."""

    name: str
    stocks: list[HotmoneyStock] = Field(default_factory=list)


class Hotmoney(BaseModel):
    """Dragon-Tiger board (hotmoney) data."""

    date: str
    total_net_yi: float | None = None
    top_net_buy: list[HotmoneyBuy] = Field(default_factory=list)
    seats: list[HotmoneySeat] = Field(default_factory=list)


# ---- Links ----


class Link(BaseModel):
    """A single navigation link to hhxg.top."""

    title: str
    url: str
    desc: str


# ---- Snapshot (root) ----


class Snapshot(BaseModel):
    """Root model — the complete daily market snapshot (schema v3)."""

    meta: SnapshotMeta
    date: str | None = None
    disclaimer: str = ""
    ai_summary: AISummary
    market: Market | None = None
    hot_themes: list[HotTheme] = Field(default_factory=list)
    sectors: list[SectorGroup] = Field(default_factory=list)
    ladder: Ladder | None = None
    ladder_detail: LadderDetail | None = None
    focus_news: list[NewsItem] = Field(default_factory=list)
    macro_news: list[NewsItem] = Field(default_factory=list)
    hotmoney: Hotmoney | None = None
    links: dict[str, Link] = Field(default_factory=dict)

    def __repr__(self) -> str:
        return f"Snapshot(date={self.date!r}, provider={self.meta.provider!r})"
