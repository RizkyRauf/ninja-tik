import asyncio
import json
from typing import Optional

import aiohttp

from tikscraper.base import TikNinjaBaseClient
from tikscraper.models import TikTokUser, TikTokResponse
from tikscraper.utils.exceptions import TokenFetchError
from config.settings import API_URL


class TikNinjaUserClient(TikNinjaBaseClient):
    """Client for fetching TikTok user data."""

    async def get_user(self, unique_id: str) -> TikTokResponse:
        """Fetch TikTok user data by username."""
        async with self._new_session() as session:
            try:
                token = await self._fetch_token(session)
            except TokenFetchError as e:
                return TikTokResponse(error=str(e))

            payload = json.dumps({
                "action": "get_user",
                "unique_id": unique_id,
            })

            async with session.post(API_URL, headers=self._api_headers(token), data=payload) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    return TikTokResponse(error=f"HTTP {resp.status}: {body}")

                result = await resp.json()
                if not result.get("ok"):
                    return TikTokResponse(error=result.get("error", "Unknown error"), raw=result)

                return TikTokResponse(
                    success=True,
                    data=TikTokUser.from_api(result["data"]["user"], result["data"]["stats"]),
                    raw=result,
                )

    async def get_users(self, unique_ids: list[str]) -> list[TikTokResponse]:
        """Fetch multiple users concurrently."""
        tasks = [self.get_user(uid) for uid in unique_ids]
        return await asyncio.gather(*tasks)
