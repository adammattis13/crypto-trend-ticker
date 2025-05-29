import streamlit as st
import requests
import time

# Fetch from Streamlit secrets
API_KEY = st.secrets.get("COINGECKO_API_KEY", None)

def fetch_top_10_cryptos(currency="usd"):
    global CACHE, CACHE_TIMESTAMP
    now = time.time()

    if now - CACHE_TIMESTAMP < CACHE_TTL and currency in CACHE:
        return CACHE[currency]

    headers = {"x-cg-pro-api-key": API_KEY} if API_KEY else {}

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": currency,
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        CACHE[currency] = data
        CACHE_TIMESTAMP = now
        return data
    except requests.RequestException as e:
        print(f"API error: {e}")
        return []
