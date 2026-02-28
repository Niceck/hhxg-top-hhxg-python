"""Shared fixtures for hhxg SDK tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture()
def snapshot_json() -> dict:
    """Load the trimmed snapshot v3 fixture as a dict."""
    path = FIXTURES_DIR / "snapshot_v3.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture()
def snapshot_bytes() -> bytes:
    """Raw bytes of the snapshot fixture (for mocking HTTP responses)."""
    path = FIXTURES_DIR / "snapshot_v3.json"
    return path.read_bytes()
