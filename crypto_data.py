import requests
import streamlit as st
import time

# Persistent cache (in module scope)
_cache = {}
_cache_timestamp = {}
CACHE_TTL = 180  # 3 minutes

def fetch_top_10_cryptos(currency="usd"):
    now = time.time()

    # Check cache validity
    if currency in _cache and now - _cache_timestamp.get(currency, 0) < CACHE_TTL:
        return _cache[currency]

    headers = {}
    api_key = st.secrets.get("COINGECKO_API_KEY", None)
    if api_key:
        headers["x-cg-pro-api-key"] = api_key

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": currency,
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        _cache[currency] = data
        _cache_timestamp[currency] = now
        return data
    except requests.RequestException as e:
        print(f"API error: {e}")
        return []

