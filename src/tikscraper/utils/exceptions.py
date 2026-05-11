class TikScraperError(Exception):
    """Base exception for tikscraper."""


class TokenFetchError(TikScraperError):
    """Failed to extract API token from page."""


class APIError(TikScraperError):
    """API returned an error response."""


class HTTPError(TikScraperError):
    """HTTP request failed."""
