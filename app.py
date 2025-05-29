import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from crypto_data import fetch_top_10_cryptos

st.set_page_config(page_title="Live Crypto Trends", layout="wide")
st.title("📈 Live Top 10 Crypto Trends")
st.markdown("Updates every minute. Displays last 4 hours of trend data.")

currency = st.selectbox("Select currency", ["usd", "eur", "btc"], index=0)

# Store history in session state
if "history" not in st.session_state:
    st.session_state.history = {}

data = fetch_top_10_cryptos(currency)
now = datetime.now()

for coin in data:
    name = coin["name"]
    price = coin["current_price"]

    if name not in st.session_state.history:
        st.session_state.history[name] = []

    # Add current price
    st.session_state.history[name].append((now, price))

    # Keep only last 4 hours
    st.session_state.history[name] = [
        (t, p) for t, p in st.session_state.history[name]
        if t > now - timedelta(hours=4)
    ]

# Plot charts
for coin in data:
    name = coin["name"]
    times, prices = zip(*st.session_state.history[name])
    df = pd.DataFrame({"Time": times, "Price": prices})
    st.line_chart(df.set_index("Time"), use_container_width=True)
