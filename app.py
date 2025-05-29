import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from crypto_data import fetch_selected_cryptos
import altair as alt

st.set_page_config(page_title="Crypto Trend Ticker", layout="wide")

st.title("📈 Top 5 Crypto Trends")
st.subheader("Past 4 Hours")
st.markdown("Live data, refreshed every minute. All prices in selected currency.")

# Currency selector
currency = st.selectbox("Select currency", ["usd", "eur", "btc"], index=0)

# Fetch live crypto data
data = fetch_selected_cryptos(currency)
now = datetime.now()

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = {}

# Build combined DataFrame
combined_df = pd.DataFrame()

for coin in data:
    name = coin.get("name")
    price = coin.get("current_price")

    if not name or price is None:
        continue

    if name not in st.session_state.history:
        st.session_state.history[name] = []

    st.session_state.history[name].append((now, price))

    # Keep only last 4 hours of history
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

# Display chart using Altair with autoscaling
if not combined_df.empty and "Time" in combined_df.columns:
    combined_df.sort_values("Time", inplace=True)
    combined_df.fillna(method="ffill", inplace=True)
    combined_df.set_index("Time", inplace=True)

    melted_df = combined_df.reset_index().melt("Time", var_name="Coin", value_name="Price")

    chart = alt.Chart(melted_df).mark_line().encode(
        x=alt.X("Time:T", title="Time"),
        y=alt.Y("Price:Q", title=f"Price ({currency.upper()})", scale=alt.Scale(zero=False)),
        color=alt.Color("Coin:N", title="Cryptocurrency")
    ).properties(
        width="container",
        height=500,
        title="Live Crypto Price Trends"
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
    st.caption("Data from CoinGecko. Autoscaled view. Updates every minute.")
else:
    st.warning("Waiting for data... Please wait a minute for initial history to build.")

# Optional: Hide Streamlit footer
st.markdown("""
    <style>
        footer {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
