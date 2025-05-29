import requests
import time
from datetime import datetime, timedelta

CACHE = {}
CACHE_TIMESTAMP = 0
CACHE_TTL = 180  # 3 minutes (limits to ~4,800 calls/month)

def fetch_top_10_cryptos(currency="usd"):
    global CACHE, CACHE_TIMESTAMP
    now = time.time()
    if now - CACHE_TIMESTAMP < CACHE_TTL and currency in CACHE:
        return CACHE[currency]

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": currency,
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        CACHE[currency] = data
        CACHE_TIMESTAMP = now
        return data
    except requests.RequestException as e:
        print(f"API error: {e}")
        return []
