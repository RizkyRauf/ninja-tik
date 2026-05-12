import re
from dataclasses import dataclass
from typing import Optional

import aiohttp

from tikscraper.utils.exceptions import TokenFetchError
from config.settings import BASE_URL, DEFAULT_HEADERS


@dataclass
class ApiResult:
    status: int
    body: str


class TikNinjaBaseClient:
    """Base client with shared token fetching and session management."""

    def __init__(self, headers: Optional[dict] = None):
        self._token: Optional[str] = None
        self._headers = headers or DEFAULT_HEADERS.copy()

    async def _fetch_token(self, session: aiohttp.ClientSession, force: bool = False) -> str:
        if self._token and not force:
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

    async def _refresh_token(self, session: aiohttp.ClientSession) -> str:
        """Force fetch a new token, discarding the cached one."""
        self._token = None
        return await self._fetch_token(session, force=True)

    def _api_headers(self, token: str) -> dict:
        return {
            "Content-Type": "application/json",
            "X-Api-Token": token,
        }

    def _new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(headers=self._headers)

    async def _post_with_retry(self, session: aiohttp.ClientSession, url: str, payload: str) -> ApiResult:
        """POST request with automatic token refresh on 403."""
        token = await self._fetch_token(session)
        headers = self._api_headers(token)

        async with session.post(url, headers=headers, data=payload) as resp:
            body = await resp.text()
            if resp.status == 403:
                token = await self._refresh_token(session)
                headers = self._api_headers(token)
                async with session.post(url, headers=headers, data=payload) as resp2:
                    return ApiResult(status=resp2.status, body=await resp2.text())
            return ApiResult(status=resp.status, body=body)
