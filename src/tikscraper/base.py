import re
from typing import Optional

import aiohttp

from tikscraper.utils.exceptions import TokenFetchError
from config.settings import BASE_URL, DEFAULT_HEADERS


class TikNinjaBaseClient:
    """Base client with shared token fetching and session management."""

    def __init__(self, headers: Optional[dict] = None):
        self._token: Optional[str] = None
        self._headers = headers or DEFAULT_HEADERS.copy()

    async def _fetch_token(self, session: aiohttp.ClientSession) -> str:
        if self._token:
            return self._token

        async with session.get(BASE_URL) as resp:
            if resp.status != 200:
                raise TokenFetchError(f"Failed to fetch page: HTTP {resp.status}")
            html = await resp.text()

        match = re.search(r'const TOKEN = "([^"]+)"', html)
        if not match:
            raise TokenFetchError("Failed to extract API token from page")

        self._token = match.group(1)
        return self._token

    def _api_headers(self, token: str) -> dict:
        return {
            "Content-Type": "application/json",
            "X-Api-Token": token,
        }

    def _new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(headers=self._headers)
