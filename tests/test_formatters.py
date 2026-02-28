"""Tests for text formatters."""

from __future__ import annotations

from hhxg.formatters import (
    format_hot_themes,
    format_hotmoney,
    format_ladder,
    format_market,
    format_news,
    format_sectors,
    format_snapshot,
)
from hhxg.models import Snapshot


class TestFormatSnapshot:
    def test_contains_date(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_snapshot(snap)
        assert "2026-02-27" in text

    def test_contains_sections(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_snapshot(snap)
        assert "市场赚钱效应" in text
        assert "热门题材" in text
        assert "连板天梯" in text
        assert "游资龙虎榜" in text
        assert "焦点新闻" in text

    def test_contains_cta(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_snapshot(snap)
        assert "hhxg.top" in text


class TestFormatMarket:
    def test_basic(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_market(snap.market)
        assert "61.8%" in text
        assert "强" in text
        assert "涨停" in text

    def test_buckets_table(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_market(snap.market)
        assert "小涨" in text
        assert "2700" in text


class TestFormatHotThemes:
    def test_table(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_hot_themes(snap.hot_themes)
        assert "绿色电力" in text
        assert "华银电力" in text
        assert "16" in text


class TestFormatSectors:
    def test_grouped(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_sectors(snap.sectors)
        assert "行业" in text
        assert "小金属" in text
        assert "强势" in text
        assert "弱势" in text


class TestFormatLadder:
    def test_levels(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_ladder(snap.ladder_detail)
        assert "7板" in text
        assert "豫能控股" in text
        assert "001896.SZ" in text

    def test_distributions(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_ladder(snap.ladder_detail)
        assert "江苏" in text


class TestFormatHotmoney:
    def test_top_buy(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_hotmoney(snap.hotmoney)
        assert "烽火通信" in text
        assert "40.96" in text

    def test_seats(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_hotmoney(snap.hotmoney)
        assert "赵老哥" in text


class TestFormatNews:
    def test_items(self, snapshot_json: dict) -> None:
        snap = Snapshot.model_validate(snapshot_json)
        text = format_news(snap.focus_news)
        assert "焦点" in text
