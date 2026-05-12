import json
from tikscraper.models import TikTokResponse, VideoListResponse
from tikscraper.models import TikTokVideo, TikTokAnalytics


def to_json(responses: list | TikTokResponse | VideoListResponse | list[TikTokVideo] | TikTokAnalytics, indent: int = 2) -> str:
    """Format one or more responses as JSON."""
    if isinstance(responses, (TikTokResponse, VideoListResponse)):
        responses = [responses]
    elif isinstance(responses, TikTokAnalytics):
        responses = [responses]

    items = []
    for r in responses:
        if isinstance(r, VideoListResponse):
            items.append(r.to_dict())
        elif isinstance(r, TikTokVideo):
            items.append(r.to_dict())
        elif isinstance(r, TikTokAnalytics):
            items.append(r.to_dict())
        elif isinstance(r, TikTokResponse):
            if r.success and r.data:
                items.append(r.data.to_dict())
            else:
                items.append({"error": r.error, "raw": r.raw})

    return json.dumps(items if len(items) != 1 else items[0], indent=indent, ensure_ascii=False)
