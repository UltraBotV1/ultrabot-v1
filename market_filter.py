import requests

def get_btc_trend():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1"  # No interval, use default (daily data points)
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        prices = data.get("prices", [])
        if len(prices) < 3:
            print("⚠️ Not enough BTC data to determine trend.")
            return []

        # Extract just the closing prices
        closes = [price[1] for price in prices[-3:]]  # last 3 prices
        return closes

    except Exception as e:
        print(f"❌ Error fetching BTC trend from CoinGecko: {e}")
        return []

def is_market_healthy():
    closes = get_btc_trend()
    if len(closes) < 3:
        print("⚠️ Not enough BTC data to determine trend.")
        return False

    if closes[2] >= closes[1] and closes[1] >= closes[0]:
        print("✅ Market is trending up.")
        return True
    else:
        print("❌ Market is not healthy.")
        return False

from volume_tracker import get_volume_spike

def is_token_trending(token):
    # Check if a token has a volume spike
    return get_volume_spike(token)