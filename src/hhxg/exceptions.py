"""Exception hierarchy for the hhxg SDK."""


class HhxgError(Exception):
    """Base exception for all hhxg errors."""


class NetworkError(HhxgError):
    """Raised when a network request fails."""


class SchemaError(HhxgError):
    """Raised when the server response does not match the expected schema."""
