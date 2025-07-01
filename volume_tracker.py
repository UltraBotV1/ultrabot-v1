import requests

def get_volume_spike(token_symbol, threshold=1.5):
    '''
    Detects a volume spike for a given token using CoinGecko's API.
    Returns True if spike is detected, else False.
    '''
    url = f"https://api.coingecko.com/api/v3/coins/{token_symbol}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        volumes = [point[1] for point in data.get("total_volumes", [])]
        if len(volumes) < 3:
            print(f"⚠️ Not enough volume data for {token_symbol}")
            return False

        # Compare last volume to average of previous
        avg_volume = sum(volumes[:-1]) / len(volumes[:-1])
        last_volume = volumes[-1]

        if last_volume > avg_volume * threshold:
            print(f"📈 Volume spike detected for {token_symbol}")
            return True
        else:
            print(f"📉 No volume spike for {token_symbol}")
            return False

    except Exception as e:
        print(f"❌ Error checking volume for {token_symbol}: {e}")
        return False