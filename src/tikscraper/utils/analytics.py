from datetime import datetime
from tikscraper.models import TikTokUser, TikTokVideo, TikTokAnalytics


def compute_analytics(user: TikTokUser, videos: list[TikTokVideo]) -> TikTokAnalytics:
    """Compute analytics from user profile and loaded videos."""
    if not videos:
        return TikTokAnalytics()

    total_views = sum(v.play_count for v in videos)
    total_likes = sum(v.digg_count for v in videos)
    total_comments = sum(v.comment_count for v in videos)
    total_shares = sum(v.share_count for v in videos)
    total_saves = sum(v.collect_count for v in videos)
    count = len(videos)

    avg_views = total_views / count
    avg_likes = total_likes / count
    avg_comments = total_comments / count
    avg_shares = total_shares / count
    avg_saves = total_saves / count

    # Engagement rate: (avg_likes + avg_comments + avg_shares + avg_saves) / followers * 100
    engagement_sum = total_likes + total_comments + total_shares + total_saves
    followers = user.stats.follower_count
    avg_engagement_rate = (engagement_sum / count) / max(followers, 1) * 100

    # Audience
    following = user.stats.following_count
    follower_following_ratio = followers / max(following, 1)
    total_likes = user.stats.heart_count

    # Content
    videos_posted = user.stats.video_count
    avg_likes_lifetime = total_likes / max(videos_posted, 1)

    account_age_days = 0
    avg_likes_per_month = 0.0
    if user.create_time:
        now = datetime.now(user.create_time.tzinfo) if user.create_time.tzinfo else datetime.now()
        delta = now - user.create_time
        account_age_days = delta.days
        months = max(account_age_days / 30.44, 1)
        avg_likes_per_month = total_likes / months

    return TikTokAnalytics(
        avg_engagement_rate=round(avg_engagement_rate, 2),
        avg_views=round(avg_views, 2),
        avg_likes=round(avg_likes, 2),
        avg_comments=round(avg_comments, 2),
        avg_shares=round(avg_shares, 2),
        avg_saves=round(avg_saves, 2),
        followers=followers,
        following=following,
        follower_following_ratio=round(follower_following_ratio, 2),
        total_likes=total_likes,
        videos_posted=videos_posted,
        avg_likes_lifetime=round(avg_likes_lifetime, 2),
        account_age_days=account_age_days,
        avg_likes_per_month=round(avg_likes_per_month, 2),
    )
