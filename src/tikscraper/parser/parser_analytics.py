from lxml import html as lxml_html

ANALYTICS_SELECTORS = {
    "engagement": {
        "rate": '//span[@class="stat-cell-val neutral"]',
        "avg_views": '(//p[@class="stats-section-title"][text()="Engagement (est. from loaded videos)"]/following-sibling::div//span[@class="stat-cell-val"])[1]',
        "avg_likes": '(//p[@class="stats-section-title"][text()="Engagement (est. from loaded videos)"]/following-sibling::div//span[@class="stat-cell-val"])[2]',
        "avg_comments": '(//p[@class="stats-section-title"][text()="Engagement (est. from loaded videos)"]/following-sibling::div//span[@class="stat-cell-val"])[3]',
        "avg_shares": '(//p[@class="stats-section-title"][text()="Engagement (est. from loaded videos)"]/following-sibling::div//span[@class="stat-cell-val"])[4]',
        "avg_saves": '(//p[@class="stats-section-title"][text()="Engagement (est. from loaded videos)"]/following-sibling::div//span[@class="stat-cell-val"])[5]',
    },
    "audience": {
        "followers": '(//p[@class="stats-section-title"][text()="Audience & Reach"]/following-sibling::div//span[@class="stat-cell-val"])[1]',
        "following": '(//p[@class="stats-section-title"][text()="Audience & Reach"]/following-sibling::div//span[@class="stat-cell-val"])[2]',
        "follower_following_ratio": '(//p[@class="stats-section-title"][text()="Audience & Reach"]/following-sibling::div//span[@class="stat-cell-val"])[3]',
        "total_likes": '(//p[@class="stats-section-title"][text()="Audience & Reach"]/following-sibling::div//span[@class="stat-cell-val"])[4]',
    },
    "content": {
        "videos_posted": '(//p[@class="stats-section-title"][text()="Content"]/following-sibling::div//span[@class="stat-cell-val"])[1]',
        "avg_likes_lifetime": '(//p[@class="stats-section-title"][text()="Content"]/following-sibling::div//span[@class="stat-cell-val"])[2]',
        "account_age": '(//p[@class="stats-section-title"][text()="Content"]/following-sibling::div//span[@class="stat-cell-val"])[3]',
        "account_age_sub": '(//p[@class="stats-section-title"][text()="Content"]/following-sibling::div//span[@class="stat-cell-sub"])[2]',
        "avg_likes_per_month": '(//p[@class="stats-section-title"][text()="Content"]/following-sibling::div//span[@class="stat-cell-val"])[4]',
    },
    "description": '//p[@class="er-note"]',
}


def extract_text(page_html: str, xpath: str) -> str | None:
    """Extract raw text from HTML using XPath. Returns None if not found."""
    tree = lxml_html.fromstring(page_html)
    result = tree.xpath(xpath)
    if result:
        text = result[0].text_content().strip()
        return text if text else None
    return None


def _parse_num(raw: str | None) -> float | None:
    if raw is None:
        return None
    s = raw.strip().rstrip("%").replace(",", "")
    multiplier = 1
    if s.endswith("M"):
        multiplier = 1_000_000
        s = s[:-1]
    elif s.endswith("B"):
        multiplier = 1_000_000_000
        s = s[:-1]
    elif s.endswith("K"):
        multiplier = 1_000
        s = s[:-1]
    s = s.replace("x", "").replace("yr", "").replace("mo", "").strip()
    try:
        return float(s) * multiplier
    except ValueError:
        return None


def _parse_int(raw: str | None) -> int | None:
    if raw is None:
        return None
    s = raw.strip().replace(",", "")
    multiplier = 1
    if s.endswith("M"):
        multiplier = 1_000_000
        s = s[:-1]
    elif s.endswith("B"):
        multiplier = 1_000_000_000
        s = s[:-1]
    elif s.endswith("K"):
        multiplier = 1_000
        s = s[:-1]
    try:
        return int(float(s) * multiplier)
    except ValueError:
        return None


def parse_engagement(page_html: str) -> dict:
    s = ANALYTICS_SELECTORS["engagement"]
    return {
        "Avg Engagement Rate": _parse_num(extract_text(page_html, s["rate"])),
        "Avg Views / Video": _parse_num(extract_text(page_html, s["avg_views"])),
        "Avg Likes / Video": _parse_num(extract_text(page_html, s["avg_likes"])),
        "Avg Comments / Video": _parse_num(extract_text(page_html, s["avg_comments"])),
        "Avg Shares / Video": _parse_num(extract_text(page_html, s["avg_shares"])),
        "Avg Saves / Video": _parse_num(extract_text(page_html, s["avg_saves"])),
    }


def parse_audience(page_html: str) -> dict:
    s = ANALYTICS_SELECTORS["audience"]
    return {
        "Followers": _parse_int(extract_text(page_html, s["followers"])),
        "Following": _parse_int(extract_text(page_html, s["following"])),
        "F / F Ratio": _parse_num(extract_text(page_html, s["follower_following_ratio"])),
        "Total Likes": _parse_int(extract_text(page_html, s["total_likes"])),
    }


def parse_content(page_html: str) -> dict:
    s = ANALYTICS_SELECTORS["content"]
    return {
        "Videos Posted": _parse_int(extract_text(page_html, s["videos_posted"])),
        "Avg Likes / Video (lifetime)": _parse_num(extract_text(page_html, s["avg_likes_lifetime"])),
        "Account Age": extract_text(page_html, s["account_age"]),
        "Account Age (since)": extract_text(page_html, s["account_age_sub"]),
        "Avg Likes / Month": _parse_num(extract_text(page_html, s["avg_likes_per_month"])),
    }


def parse_description(page_html: str) -> str | None:
    return extract_text(page_html, ANALYTICS_SELECTORS["description"])


def parse_analytics(page_html: str) -> dict:
    """Parse full analytics from rendered HTML. Returns structured dict."""
    return {
        "Engagement": parse_engagement(page_html),
        "Audience": parse_audience(page_html),
        "Content": parse_content(page_html),
        "Description": parse_description(page_html),
    }
