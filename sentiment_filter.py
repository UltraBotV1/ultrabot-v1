# clean_sentiment_filter.py

import time
from datetime import datetime, timedelta

VOLUME_SPIKE_THRESHOLD = 1.5  # 150% increase
BTC_TREND_LOOKBACK_HOURS = 1
BTC_TREND_MIN_PERCENT = 1.0  # % change to consider bullish/bearish

def fetch_volume_data(token_id, market_data):
    try:
        volumes = market_data.get(token_id.upper(), {}).get("volumes", [])
        return volumes
    except Exception as e:
        print(f"❌ Error checking volume for {token_id}: {e}")
        return None

def is_volume_spike(volumes):
    if len(volumes) < 2:
        return False
    recent_vol = volumes[-1]
    past_avg = sum(volumes[-25:-1]) / len(volumes[-25:-1])
    spike = recent_vol > past_avg * VOLUME_SPIKE_THRESHOLD
    print(f"📈 Volume spike? {spike} (Recent: {recent_vol:.2f}, Avg: {past_avg:.2f})")
    return spike

def get_btc_trend(prices):
    try:
        if not prices:
            return "neutral"
        avg_past_price = sum(p[1] for p in prices[:-1]) / len(prices[:-1])
        current_price = prices[-1][1]
        change_percent = ((current_price - avg_past_price) / avg_past_price) * 100

        print(f"📉 BTC 1h Trend: {change_percent:.2f}%")
        if change_percent > BTC_TREND_MIN_PERCENT:
            return "bullish"
        elif change_percent < -BTC_TREND_MIN_PERCENT:
            return "bearish"
        return "neutral"
    except Exception as e:
        print(f"❌ Error determining BTC trend: {e}")
        return "neutral"

def should_trade(token_id, market_data, btc_prices):
    print(f"\n🔍 Analyzing {token_id.upper()}...")
    volumes = fetch_volume_data(token_id, market_data)
    if not volumes:
        return False

    volume_spike = is_volume_spike(volumes)
    btc_trend = get_btc_trend(btc_prices)

    print(f"📊 Market Sentiment Filter → Volume: {volume_spike}, BTC Trend: {btc_trend}")
    if volume_spike and btc_trend != "bearish":
        print(f"✅ Conditions met. Ready to trade {token_id.upper()}")
        return True

    print(f"⛔ Conditions not favorable. Skipping {token_id.upper()}")
    return False