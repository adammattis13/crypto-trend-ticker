import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from crypto_data import fetch_top_10_cryptos

st.set_page_config(page_title="Crypto Trend Ticker", layout="wide")
st.title("📈 Top 5 Crypto Trends")
st.subheader("Past 4 Hours")
st.markdown("Live data, refreshed every minute. All prices in selected currency.")

currency = st.selectbox("Select currency", ["usd", "eur", "btc"], index=0)

# Get top 5 cryptos only
data = fetch_top_10_cryptos(currency)[:5]
now = datetime.now()

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = {}

# Build 5-line dataframe
combined_df = pd.DataFrame()

for coin in data:
    name = coin["name"]
    price = coin["current_price"]

    if name not in st.session_state.history:
        st.session_state.history[name] = []

    st.session_state.history[name].append((now, price))

    # Trim to last 4 hours
    st.session_state.history[name] = [
        (t, p) for t, p in st.session_state.history[name]
        if t > now - timedelta(hours=4)
    ]

    temp_df = pd.DataFrame({
        "Time": [t for t, _ in st.session_state.history[name]],
        name: [p for _, p in st.session_state.history[name]],
    })

    if combined_df.empty:
        combined_df = temp_df
    else:
        combined_df = pd.merge(combined_df, temp_df, on="Time", how="outer")

# Clean and display
combined_df.sort_values("Time", inplace=True)
combined_df.fillna(method="ffill", inplace=True)
combined_df.set_index("Time", inplace=True)

st.line_chart(combined_df, use_container_width=True)
st.caption("Data from CoinGecko. Updates every minute. Lines represent the top 5 cryptocurrencies by market cap.")
