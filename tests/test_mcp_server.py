"""Tests for the MCP server tool functions."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from hhxg.models import Snapshot


# Only run if mcp is installed
pytest.importorskip("mcp")

from hhxg.mcp_server import (  # noqa: E402
    _client,
    get_hot_themes,
    get_hotmoney,
    get_ladder,
    get_market,
    get_news,
    get_sectors,
    get_snapshot,
)


@pytest.fixture()
def _mock_snapshot(snapshot_json: dict):
    """Patch the MCP server's client to return fixture data."""
    snap = Snapshot.model_validate(snapshot_json)
    with patch.object(_client, "get_snapshot", return_value=snap):
        yield snap


class TestMcpTools:
    @pytest.mark.usefixtures("_mock_snapshot")
    def test_get_snapshot(self) -> None:
        result = get_snapshot()
        assert "2026-02-27" in result
        assert "市场赚钱效应" in result
        assert "hhxg.top" in result

    @pytest.mark.usefixtures("_mock_snapshot")
    def test_get_market(self) -> None:
        result = get_market()
        assert "61.8%" in result

    @pytest.mark.usefixtures("_mock_snapshot")
    def test_get_hot_themes(self) -> None:
        result = get_hot_themes()
        assert "绿色电力" in result

    @pytest.mark.usefixtures("_mock_snapshot")
    def test_get_sectors(self) -> None:
        result = get_sectors()
        assert "小金属" in result

    @pytest.mark.usefixtures("_mock_snapshot")
    def test_get_ladder(self) -> None:
        result = get_ladder()
        assert "豫能控股" in result

    @pytest.mark.usefixtures("_mock_snapshot")
    def test_get_hotmoney(self) -> None:
        result = get_hotmoney()
        assert "烽火通信" in result

    @pytest.mark.usefixtures("_mock_snapshot")
    def test_get_news(self) -> None:
        result = get_news()
        assert "焦点" in result
