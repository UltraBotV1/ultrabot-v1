import requests
import json

url = "https://api.blofin.com/api/v1/futures/public/market/ticker?symbol=BTC-USDT"

headers = {
    "User-Agent": "Mozilla/5.0",  # Prevents 403 errors from some endpoints
    "Content-Type": "application/json"
}

print(f"\n🔍 Fetching price from: {url}")
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(f"📦 API Response:\n{json.dumps(data, indent=2)}")

    if data.get("code") == "00000":
        price = float(data["data"][0]["asks"][0][0])
        print(f"✅ BTC Price: {price}")
    else:
        print(f"❌ Error: {data}")
except Exception as e:
    print(f"❌ Exception: {e}")