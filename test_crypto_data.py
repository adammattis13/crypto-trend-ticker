from crypto_data import fetch_top_10_cryptos

def test_fetch_top_10():
    data = fetch_top_10_cryptos("usd")
    assert isinstance(data, list)
    assert len(data) <= 10
    for coin in data:
        assert "name" in coin
        assert "current_price" in coin
