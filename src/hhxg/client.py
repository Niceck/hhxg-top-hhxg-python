"""HTTP client for fetching the hhxg daily snapshot."""

from __future__ import annotations

import httpx
from pydantic import ValidationError

from ._constants import DEFAULT_TIMEOUT, SNAPSHOT_URL
from .exceptions import NetworkError, SchemaError
from .models import Snapshot


class HhxgClient:
    """Synchronous client that fetches and caches the daily snapshot.

    The snapshot is cached in memory for the same trading date so repeated
    calls within a session do not trigger extra HTTP requests.

    Parameters
    ----------
    base_url:
        Override the default snapshot URL (useful for testing or mirrors).
    timeout:
        HTTP request timeout in seconds.
    """

    def __init__(
        self,
        base_url: str = SNAPSHOT_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._url = base_url
        self._timeout = timeout
        self._cached: Snapshot | None = None

    # -- public API --

    def get_snapshot(self, *, force: bool = False) -> Snapshot:
        """Fetch and return the full daily snapshot.

        Parameters
        ----------
        force:
            If ``True``, bypass the in-memory cache and always fetch from
            the remote server.
        """
        if self._cached is not None and not force:
            return self._cached

        data = self._fetch_json()
        snapshot = self._parse(data)
        self._cached = snapshot
        return snapshot

    def clear_cache(self) -> None:
        """Drop the cached snapshot so the next call re-fetches."""
        self._cached = None

    # -- internal helpers --

    def _fetch_json(self) -> dict:
        try:
            with httpx.Client(timeout=self._timeout) as http:
                resp = http.get(self._url)
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as exc:
            raise NetworkError(
                f"HTTP {exc.response.status_code} from {self._url}"
            ) from exc
        except httpx.RequestError as exc:
            raise NetworkError(f"Request failed: {exc}") from exc

    @staticmethod
    def _parse(data: dict) -> Snapshot:
        try:
            return Snapshot.model_validate(data)
        except ValidationError as exc:
            raise SchemaError(f"Schema validation failed: {exc}") from exc
