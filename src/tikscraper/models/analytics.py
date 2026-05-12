from dataclasses import dataclass, asdict


@dataclass
class TikTokAnalytics:
    # Engagement (from loaded videos)
    avg_engagement_rate: float = 0.0
    avg_views: float = 0.0
    avg_likes: float = 0.0
    avg_comments: float = 0.0
    avg_shares: float = 0.0
    avg_saves: float = 0.0

    # Audience & Reach
    followers: int = 0
    following: int = 0
    follower_following_ratio: float = 0.0
    total_likes: int = 0

    # Content
    videos_posted: int = 0
    avg_likes_lifetime: float = 0.0
    account_age_days: int = 0
    avg_likes_per_month: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)
