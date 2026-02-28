"""Tests for Pydantic model serialization / deserialization."""

from __future__ import annotations

import pytest

from hhxg.models import (
    Bucket,
    Hotmoney,
    HotmoneyBuy,
    HotmoneySeat,
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
    TopStock,
)


class TestSnapshot:
    """Root snapshot model round-trip."""

    def test_parse_fixture(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        assert snap.date == "2026-02-27"
        assert snap.meta.provider == "hhxg.top"
        assert snap.meta.schema_version == 3

    def test_repr(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        assert "hhxg.top" in repr(snap)
        assert "2026-02-27" in repr(snap)

    def test_round_trip(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        exported = snap.model_dump()
        snap2 = Snapshot.model_validate(exported)
        assert snap2.date == snap.date
        assert snap2.meta.provider == snap.meta.provider


class TestMarket:
    def test_parse(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        m = snap.market
        assert m is not None
        assert m.sentiment_index == 61.8
        assert m.sentiment_label == "强"
        assert m.limit_up == 75
        assert m.fried == 31
        assert m.total == 5299

    def test_buckets(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        assert len(snap.market.buckets) == 2
        b = snap.market.buckets[0]
        assert b.name == "小涨"
        assert b.count == 2700

    def test_optional_fields(self) -> None:
        m = Market(date="2026-01-01", sentiment_index=50.0, sentiment_label="中")
        assert m.limit_up is None
        assert m.buckets == []


class TestHotThemes:
    def test_parse(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        assert len(snap.hot_themes) == 2
        t = snap.hot_themes[0]
        assert t.name == "绿色电力"
        assert t.limitup_count == 16

    def test_top_stocks(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        stocks = snap.hot_themes[0].top_stocks
        assert len(stocks) == 2
        assert stocks[0].name == "华银电力"


class TestSectors:
    def test_parse(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        assert len(snap.sectors) == 1
        g = snap.sectors[0]
        assert g.label == "行业"
        assert len(g.strong) == 1
        assert g.strong[0].name == "小金属"
        assert g.strong[0].net_yi == 78.0

    def test_weak(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        w = snap.sectors[0].weak
        assert len(w) == 1
        assert w[0].net_yi == -12.0


class TestLadder:
    def test_summary(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        assert snap.ladder is not None
        assert snap.ladder.max_streak == 7
        assert snap.ladder.top_streak.name == "豫能控股"

    def test_detail(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        d = snap.ladder_detail
        assert d is not None
        assert len(d.levels) == 2
        assert d.levels[0].boards == 7
        assert d.levels[0].stocks[0].code == "001896.SZ"

    def test_distributions(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        d = snap.ladder_detail
        assert d.lb_rates_map["7"] == "100.0%"
        assert d.area_counts["江苏"] == 10
        assert d.concept_counts["风电"] == 16


class TestHotmoney:
    def test_parse(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        hm = snap.hotmoney
        assert hm is not None
        assert hm.total_net_yi == 40.96
        assert len(hm.top_net_buy) == 2
        assert hm.top_net_buy[0].name == "烽火通信"

    def test_seats(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        seats = snap.hotmoney.seats
        assert len(seats) == 1
        assert seats[0].name == "赵老哥"
        assert len(seats[0].stocks) == 2


class TestNews:
    def test_focus(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        assert len(snap.focus_news) == 2
        assert snap.focus_news[0].cat == "焦点"

    def test_macro(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        assert len(snap.macro_news) == 1
        assert snap.macro_news[0].cat == "宏观"


class TestLinks:
    def test_parse(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        assert "full_report" in snap.links
        assert snap.links["website"].url == "https://hhxg.top"


class TestAISummary:
    def test_parse(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        s = snap.ai_summary
        assert "61.8%" in s.market_state
        assert "恢恢量化" in s.cta
