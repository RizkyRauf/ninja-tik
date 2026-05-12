from pydantic import BaseModel


class UserStats(BaseModel):
    following_count: int
    follower_count: int
    heart_count: int
    video_count: int
    digg_count: int


class UserData(BaseModel):
    id: str
    unique_id: str
    nickname: str
    signature: str
    avatar: str
    verified: bool
    private_account: bool
    sec_uid: str
    bio_email: str
    create_time: str | None
    stats: UserStats


class UserResponse(BaseModel):
    success: bool
    data: UserData | None = None
    error: str | None = None


class VideoResponse(BaseModel):
    success: bool
    data: list[dict] | None = None
    error: str | None = None


class MultiUserVideoResponse(BaseModel):
    success: bool
    data: dict[str, list[dict]] | None = None
    error: str | None = None


class AnalyticsResponse(BaseModel):
    success: bool
    data: dict | None = None
    error: str | None = None
