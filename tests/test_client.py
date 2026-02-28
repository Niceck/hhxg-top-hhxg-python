"""Tests for HhxgClient (mocked HTTP)."""

from __future__ import annotations

import json
from unittest.mock import patch

import httpx
import pytest

from hhxg.client import HhxgClient
from hhxg.exceptions import NetworkError, SchemaError


class TestHhxgClient:
    """Client unit tests — mock at _fetch_json / _parse level."""

    def test_get_snapshot_success(self, snapshot_json: dict) -> None:
        client = HhxgClient()
        with patch.object(client, "_fetch_json", return_value=snapshot_json):
            snap = client.get_snapshot()
            assert snap.date == "2026-02-27"
            assert snap.meta.schema_version == 3

    def test_cache_hit(self, snapshot_json: dict) -> None:
        client = HhxgClient()
        call_count = 0
        original = client._fetch_json

        def counting_fetch():
            nonlocal call_count
            call_count += 1
            return snapshot_json

        with patch.object(client, "_fetch_json", side_effect=counting_fetch):
            snap1 = client.get_snapshot()
            snap2 = client.get_snapshot()
            assert snap1.date == snap2.date
            assert call_count == 1

    def test_force_refetch(self, snapshot_json: dict) -> None:
        client = HhxgClient()
        call_count = 0

        def counting_fetch():
            nonlocal call_count
            call_count += 1
            return snapshot_json

        with patch.object(client, "_fetch_json", side_effect=counting_fetch):
            client.get_snapshot()
            client.get_snapshot(force=True)
            assert call_count == 2

    def test_clear_cache(self, snapshot_json: dict) -> None:
        client = HhxgClient()
        call_count = 0

        def counting_fetch():
            nonlocal call_count
            call_count += 1
            return snapshot_json

        with patch.object(client, "_fetch_json", side_effect=counting_fetch):
            client.get_snapshot()
            client.clear_cache()
            client.get_snapshot()
            assert call_count == 2

    def test_network_error_on_http_error(self) -> None:
        client = HhxgClient()

        def raise_network():
            raise NetworkError("HTTP 500 from https://hhxg.top/...")

        with patch.object(client, "_fetch_json", side_effect=raise_network):
            with pytest.raises(NetworkError, match="500"):
                client.get_snapshot()

    def test_network_error_on_connection_failure(self) -> None:
        client = HhxgClient()

        def raise_network():
            raise NetworkError("Request failed: Connection refused")

        with patch.object(client, "_fetch_json", side_effect=raise_network):
            with pytest.raises(NetworkError, match="Connection refused"):
                client.get_snapshot()

    def test_schema_error_on_invalid_json(self) -> None:
        client = HhxgClient()
        with patch.object(client, "_fetch_json", return_value={"meta": {}}):
            with pytest.raises(SchemaError):
                client.get_snapshot()

    def test_custom_base_url(self, snapshot_json: dict) -> None:
        custom_url = "https://mirror.example.com/snapshot.json"
        client = HhxgClient(base_url=custom_url)
        assert client._url == custom_url
        with patch.object(client, "_fetch_json", return_value=snapshot_json):
            snap = client.get_snapshot()
            assert snap.date == "2026-02-27"

    def test_parse_valid(self, snapshot_json: dict) -> None:
        snap = HhxgClient._parse(snapshot_json)
        assert snap.date == "2026-02-27"

    def test_parse_invalid(self) -> None:
        with pytest.raises(SchemaError):
            HhxgClient._parse({"not": "a snapshot"})
