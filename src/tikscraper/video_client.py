import asyncio
import json
from typing import Optional

import aiohttp

from tikscraper.base import TikNinjaBaseClient
from tikscraper.models import TikTokVideo, VideoListResponse
from tikscraper.user_client import TikNinjaUserClient
from tikscraper.utils.exceptions import TokenFetchError
from config.settings import API_URL


class TikNinjaVideoClient(TikNinjaBaseClient):
    """Client for fetching TikTok video data."""

    async def _resolve_user_ids(self, unique_ids: list[str]) -> dict[str, str]:
        """Resolve multiple usernames to user IDs concurrently."""
        user_client = TikNinjaUserClient(headers=self._headers)
        results = await user_client.get_users(unique_ids)

        mapping = {}
        for username, result in zip(unique_ids, results):
            if result.success:
                mapping[username] = result.data.id
        return mapping

    async def get_posts(self, user_id: str = "", unique_id: str = "", cursor: str = "0", count: int = 20) -> VideoListResponse:
        """Fetch one page of TikTok user videos."""
        if unique_id and not user_id:
            resolved = await self._resolve_user_ids([unique_id])
            user_id = resolved.get(unique_id)
            if not user_id:
                return VideoListResponse(error=f"User '{unique_id}' not found")

        async with self._new_session() as session:
            try:
                await self._fetch_token(session)
            except TokenFetchError as e:
                return VideoListResponse(error=str(e))

            payload = json.dumps({
                "action": "get_posts",
                "user_id": user_id,
                "cursor": cursor,
                "count": count,
            })

            result_data = await self._post_with_retry(session, API_URL, payload)
            if result_data.status != 200:
                return VideoListResponse(error=f"HTTP {result_data.status}: {result_data.body}")

            result = json.loads(result_data.body)
            if not result.get("ok"):
                return VideoListResponse(error=result.get("error", "Unknown error"), raw=result)

            videos = [TikTokVideo.from_api(v) for v in result["data"]["videos"]]

            return VideoListResponse(
                success=True,
                videos=videos,
                cursor=result["data"].get("cursor", ""),
                has_more=result["data"].get("hasMore", False),
                raw=result,
            )

    async def get_all_posts(self, user_id: str = "", unique_id: str = "", limit: int = 0, page_size: int = 20) -> list[TikTokVideo]:
        """Fetch all or limited number of videos with auto-pagination."""
        if unique_id and not user_id:
            resolved = await self._resolve_user_ids([unique_id])
            user_id = resolved.get(unique_id)
            if not user_id:
                return []

        all_videos: list[TikTokVideo] = []
        cursor = "0"

        while True:
            result = await self.get_posts(user_id=user_id, cursor=cursor, count=page_size)
            if not result.success:
                break

            all_videos.extend(result.videos)

            if limit and len(all_videos) >= limit:
                all_videos = all_videos[:limit]
                break

            if not result.has_more:
                break

            cursor = result.cursor

        return all_videos

    async def get_all_posts_multi(self, unique_ids: list[str], limit: int = 0, page_size: int = 20) -> dict[str, list[TikTokVideo]]:
        """Fetch videos for multiple usernames concurrently."""
        resolved = await self._resolve_user_ids(unique_ids)

        async def fetch_user(username: str, uid: str) -> tuple[str, list[TikTokVideo]]:
            videos = await self.get_all_posts(user_id=uid, limit=limit, page_size=page_size)
            return username, videos

        tasks = [fetch_user(username, uid) for username, uid in resolved.items()]
        results = await asyncio.gather(*tasks)

        return dict(results)
