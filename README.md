# tikscraper

Scraper data TikTok melalui API [tik.ninja](https://tik.ninja/). Ambil profil user, video, dan analitik akun dengan fitur refresh token otomatis dan pagination.

## Fitur

- **Pencarian user** — ambil info profil, statistik, dan bio berdasarkan username
- **Scraping video** — ambil video user dengan auto-pagination dan dukungan multi-user secara bersamaan
- **Analitik akun** — ambil engagement rate, metrik audiens, dan statistik konten melalui browser
- **Refresh token otomatis** — menangani error 403 dengan mengambil token baru secara transparan
- **Output JSON** — semua data bisa diserialkan ke JSON untuk integrasi mudah
- **Typed dataclasses** — type hints lengkap untuk autocomplete IDE

## Instalasi

```bash
# Clone repo
git clone https://github.com/RizkyRauf/ninja-tik.git
cd ninja-tik

# Buat virtual environment
python -m venv venv
source venv/bin/activate

# Install semua dependencies
pip install -r requirements.txt

# ATAU install package saja (tanpa API)
pip install -e .
```

## Konfigurasi

Salin file contoh env dan sesuaikan nilainya:

```bash
cp .env.example .env
```

```env
BASE_URL=https://tik.ninja/
API_URL=https://tik.ninja/api.php
API_TOKEN=REPLACE_WITH_64_RANDOM_CHARS
```

## Penggunaan Cepat

### Ambil Profil User

```python
import asyncio
from tikscraper import TikNinjaUserClient, to_json

async def main():
    client = TikNinjaUserClient()
    result = await client.get_user("angelinawj")

    if result.success:
        print(to_json(result))

asyncio.run(main())
```

### Ambil Video User

```python
import asyncio
from tikscraper import TikNinjaVideoClient, to_json

async def main():
    client = TikNinjaVideoClient()

    # Berdasarkan username (otomatis resolve ke user_id)
    videos = await client.get_all_posts(unique_id="angelinawj", limit=10)
    print(to_json(videos))

    # Berdasarkan user_id (lebih cepat, tanpa lookup)
    videos = await client.get_all_posts(user_id="5831967", limit=10)
    print(to_json(videos))

asyncio.run(main())
```

### Ambil Banyak User Secara Bersamaan

```python
import asyncio
from tikscraper import TikNinjaVideoClient, to_json

async def main():
    client = TikNinjaVideoClient()

    results = await client.get_all_posts_multi(
        ["angelinawj", "charlidamelio"],
        limit=5
    )

    for username, videos in results.items():
        print(f"@{username}: {len(videos)} video")
        print(to_json(videos))

asyncio.run(main())
```

### Ambil Analitik Akun

```python
import asyncio
import json
from tikscraper import scrape_analytics_cdp

async def main():
    analytics = await scrape_analytics_cdp("angelinawj")
    print(json.dumps(analytics, indent=2))

asyncio.run(main())
```

Output:

```json
{
  "Engagement": {
    "Avg Engagement Rate": 3.52,
    "Avg Views / Video": 8400000.0,
    "Avg Likes / Video": 130400.0,
    "Avg Comments / Video": 2800.0,
    "Avg Shares / Video": 16100.0,
    "Avg Saves / Video": 33700.0
  },
  "Audience": {
    "Followers": 5200000,
    "Following": 20,
    "F / F Ratio": 260639.6,
    "Total Likes": 103800000
  },
  "Content": {
    "Videos Posted": 2900,
    "Avg Likes / Video (lifetime)": 35800.0,
    "Account Age": "6.3 yrs",
    "Account Age (since)": "Jan 2020",
    "Avg Likes / Month": 1400000.0
  },
  "Description": "Based on 20 videos loaded · Average: industry average is 2–5% for large accounts."
}
```

## Referensi API

### TikNinjaUserClient

| Method | Deskripsi |
|--------|-----------|
| `get_user(unique_id)` | Ambil profil satu user |
| `get_users([unique_ids])` | Ambil banyak user secara bersamaan |

### TikNinjaVideoClient

| Method | Deskripsi |
|--------|-----------|
| `get_posts(user_id, unique_id, cursor, count)` | Ambil satu halaman video |
| `get_all_posts(user_id, unique_id, limit, page_size)` | Ambil video dengan auto-pagination |
| `get_all_posts_multi([unique_ids], limit, page_size)` | Ambil video banyak user secara bersamaan |

### Analitik

| Fungsi | Deskripsi |
|--------|-----------|
| `scrape_analytics_cdp(unique_id)` | Ambil analitik melalui SeleniumBase CDP mode |

## REST API

Project juga menyediakan REST API menggunakan FastAPI.

```bash
# Install dependencies API
pip install -r requirements.txt

# Jalankan server
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Server berjalan di `http://localhost:8000`. Dokumentasi interaktif tersedia di `http://localhost:8000/docs`.

### Endpoint

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/user/{username}` | Ambil profil user |
| GET | `/api/users?usernames=a,b,c` | Ambil banyak user |
| GET | `/api/videos/{username}?limit=20` | Ambil video user |
| GET | `/api/videos/multi?usernames=a,b,c&limit=5` | Ambil video banyak user |
| GET | `/api/analytics/{username}` | Ambil analitik akun |
| GET | `/health` | Health check |

### Contoh Request

```bash
# Ambil profil user
curl http://localhost:8000/api/user/angelinawj

# Ambil 10 video
curl "http://localhost:8000/api/videos/angelinawj?limit=10"

# Ambil video banyak user
curl "http://localhost:8000/api/videos/multi?usernames=angelinawj,charlidamelio&limit=5"

# Ambil analitik
curl http://localhost:8000/api/analytics/angelinawj
```

## Struktur Project

```
tiktok_alternatif/
├── api/
│   └── main.py              # FastAPI REST API server
├── config/
│   ├── __init__.py
│   └── settings.py          # Konfigurasi environment
├── src/tikscraper/
│   ├── __init__.py          # Export API publik
│   ├── base.py              # Shared token fetch, session, retry logic
│   ├── user_client.py       # TikNinjaUserClient
│   ├── video_client.py      # TikNinjaVideoClient
│   ├── analytics_client.py  # scrape_analytics_cdp()
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # TikTokUser, TikTokResponse
│   │   └── video.py         # TikTokVideo, VideoListResponse
│   ├── parser/
│   │   ├── __init__.py
│   │   └── parser_analytics.py  # XPath selectors (update di sini jika website berubah)
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py    # Custom exceptions
│       └── formatter.py     # to_json()
├── .env                     # Konfigurasi Anda (gitignored)
├── .env.example
├── pyproject.toml
├── requirements.txt
├── README.md
└── main_search.py           # Contoh entry point
```

## Penanganan Error

```python
from tikscraper import TikNinjaUserClient, TokenFetchError, APIError

client = TikNinjaUserClient()
result = await client.get_user("nonexistent_user_12345")

if not result.success:
    print(f"Error: {result.error}")
```

## Catatan

- **Refresh token** — ditangani otomatis. Jika request mengembalikan 403, client akan mengambil token baru dan retry sekali.
- **Rate limiting** — bersikap sopan. Tambahkan delay antar request jika scraping data dalam jumlah besar.
- **Analitik** membutuhkan `seleniumbase` dan instalasi Chrome/Chromium yang berfungsi.
- **Parser selectors** di `parser/parser_analytics.py` bisa di-update jika struktur HTML website berubah.

## Lisensi

MIT
