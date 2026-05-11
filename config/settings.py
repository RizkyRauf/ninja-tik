import os
from pathlib import Path
from fake_useragent import UserAgent

_env_path = Path(__file__).resolve().parents[1] / ".env"

if _env_path.exists():
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

BASE_URL = os.getenv("BASE_URL", "")
API_URL = os.getenv("API_URL", "")
API_TOKEN = os.getenv("API_TOKEN", "")

USER_AGENT = UserAgent(platforms="desktop").random

DEFAULT_HEADERS = {
    "User-Agent": f"{USER_AGENT}",
    "Origin": BASE_URL,
    "Referer": BASE_URL,
}
