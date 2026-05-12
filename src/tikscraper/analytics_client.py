from tikscraper.parser import parse_analytics
from seleniumbase import SB


def scrape_analytics_cdp(unique_id: str) -> dict:
    """Scrape Account Analytics from tik.ninja using CDP mode."""
    with SB(uc=True, test=True, headless=True) as sb:
        sb.activate_cdp_mode("https://tik.ninja/")
        sb.sleep(2)

        sb.cdp.click("#search-input")
        sb.sleep(0.5)
        sb.cdp.type("#search-input", f"@{unique_id}")
        sb.sleep(1)
        sb.cdp.click("#search-btn")
        sb.sleep(10)

        page_html = sb.cdp.get_html()

    return parse_analytics(page_html)
