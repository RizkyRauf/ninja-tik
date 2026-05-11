from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class TikTokUserStats:
    following_count: int = 0
    follower_count: int = 0
    heart_count: int = 0
    video_count: int = 0
    digg_count: int = 0

    @classmethod
    def from_api(cls, data: dict) -> "TikTokUserStats":
        return cls(
            following_count=data.get("followingCount", 0),
            follower_count=data.get("followerCount", 0),
            heart_count=data.get("heartCount", 0),
            video_count=data.get("videoCount", 0),
            digg_count=data.get("diggCount", 0),
        )


@dataclass
class TikTokUser:
    id: str = ""
    unique_id: str = ""
    nickname: str = ""
    signature: str = ""
    avatar: str = ""
    verified: bool = False
    private_account: bool = False
    sec_uid: str = ""
    bio_email: str = ""
    create_time: Optional[datetime] = None
    stats: TikTokUserStats = field(default_factory=TikTokUserStats)

    @classmethod
    def from_api(cls, user: dict, stats: dict) -> "TikTokUser":
        return cls(
            id=user.get("id", ""),
            unique_id=user.get("uniqueId", ""),
            nickname=user.get("nickname", ""),
            signature=user.get("signature", ""),
            avatar=user.get("avatarMedium", ""),
            verified=user.get("verified", False),
            private_account=user.get("privateAccount", False),
            sec_uid=user.get("secUid", ""),
            bio_email=user.get("bio_email", ""),
            create_time=datetime.fromtimestamp(user["createTime"]) if user.get("createTime") else None,
            stats=TikTokUserStats.from_api(stats),
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        data["create_time"] = self.create_time.isoformat() if self.create_time else None
        return data


@dataclass
class TikTokResponse:
    success: bool = False
    data: Optional[TikTokUser] = None
    error: Optional[str] = None
    raw: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "data": self.data.to_dict() if self.data else None,
            "error": self.error,
            "raw": self.raw,
        }
