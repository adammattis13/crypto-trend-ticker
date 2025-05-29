# 🔥 Crypto Trend Ticker

A live-updating crypto ticker built with Streamlit, tracking the top 10 coins over the past 4 hours. Refreshes every minute and respects API call limits.

### 🚀 Features
- Top 10 by market cap from CoinGecko
- Line charts over past 4 hours
- Currency toggle (USD, EUR, BTC)
- Auto-refresh every minute (cached every 3 min to limit API calls)

### 🛠 Setup
```bash
git clone https://github.com/yourusername/crypto-trend-ticker.git
cd crypto-trend-ticker
pip install -r requirements.txt
streamlit run app.py
