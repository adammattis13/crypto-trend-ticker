import requests
import streamlit as st
import time

# Persistent cache
_cache = {}
_cache_timestamp = {}
CACHE_TTL = 180  # seconds (3 minutes)

def fetch_selected_cryptos(currency="usd"):
    now = time.time()

    # Serve from cache if valid
    if currency in _cache and now - _cache_timestamp.get(currency, 0) < CACHE_TTL:
        return _cache[currency]

    # Removed BTC for better visual range
    coins = ["ethereum", "binancecoin", "ripple", "cardano", "solana"]
    ids = ",".join(coins)

    headers = {}

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": currency,
        "ids": ids,
        "order": "market_cap_desc",
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
