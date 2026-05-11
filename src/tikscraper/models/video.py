from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class TikTokVideoAuthor:
    id: str = ""
    unique_id: str = ""
    nickname: str = ""
    avatar: str = ""

    @classmethod
    def from_api(cls, data: dict) -> "TikTokVideoAuthor":
        return cls(
            id=data.get("id", ""),
            unique_id=data.get("unique_id", ""),
            nickname=data.get("nickname", ""),
            avatar=data.get("avatar", ""),
        )


@dataclass
class TikTokVideoMusic:
    id: str = ""
    title: str = ""
    play: str = ""
    cover: str = ""
    author: str = ""
    original: bool = False
    duration: int = 0
    album: str = ""

    @classmethod
    def from_api(cls, data: dict) -> "TikTokVideoMusic":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            play=data.get("play", ""),
            cover=data.get("cover", ""),
            author=data.get("author", ""),
            original=data.get("original", False),
            duration=data.get("duration", 0),
            album=data.get("album", ""),
        )


@dataclass
class TikTokVideo:
    aweme_id: str = ""
    video_id: str = ""
    title: str = ""
    cover: str = ""
    origin_cover: str = ""
    play: str = ""
    wmplay: str = ""
    music: str = ""
    duration: int = 0
    region: str = ""
    size: int = 0
    wm_size: int = 0
    play_count: int = 0
    digg_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    download_count: int = 0
    collect_count: int = 0
    create_time: Optional[datetime] = None
    is_ad: bool = False
    is_top: int = 0
    music_info: Optional[TikTokVideoMusic] = None
    author: Optional[TikTokVideoAuthor] = None
    _play_token: str = ""
    _music_token: str = ""

    @classmethod
    def from_api(cls, data: dict) -> "TikTokVideo":
        return cls(
            aweme_id=data.get("aweme_id", ""),
            video_id=data.get("video_id", ""),
            title=data.get("title", ""),
            cover=data.get("cover", ""),
            origin_cover=data.get("origin_cover", ""),
            play=data.get("play", ""),
            wmplay=data.get("wmplay", ""),
            music=data.get("music", ""),
            duration=data.get("duration", 0),
            region=data.get("region", ""),
            size=data.get("size", 0),
            wm_size=data.get("wm_size", 0),
            play_count=data.get("play_count", 0),
            digg_count=data.get("digg_count", 0),
            comment_count=data.get("comment_count", 0),
            share_count=data.get("share_count", 0),
            download_count=data.get("download_count", 0),
            collect_count=data.get("collect_count", 0),
            create_time=datetime.fromtimestamp(data["create_time"]) if data.get("create_time") else None,
            is_ad=data.get("is_ad", False),
            is_top=data.get("is_top", 0),
            music_info=TikTokVideoMusic.from_api(data["music_info"]) if data.get("music_info") else None,
            author=TikTokVideoAuthor.from_api(data["author"]) if data.get("author") else None,
            _play_token=data.get("_play_token", ""),
            _music_token=data.get("_music_token", ""),
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        data["create_time"] = self.create_time.isoformat() if self.create_time else None
        return data


@dataclass
class VideoListResponse:
    success: bool = False
    videos: list[TikTokVideo] = field(default_factory=list)
    cursor: str = ""
    has_more: bool = False
    error: Optional[str] = None
    raw: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "videos": [v.to_dict() for v in self.videos],
            "cursor": self.cursor,
            "has_more": self.has_more,
            "error": self.error,
            "raw": self.raw,
        }
