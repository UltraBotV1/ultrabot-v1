# blofin_api.py

import os
import requests
import time
import hmac
import hashlib
import json

BLOFIN_API_URL = os.getenv("BLOFIN_API_URL")
BLOFIN_API_KEY = os.getenv("BLOFIN_API_KEY")
BLOFIN_API_SECRET = os.getenv("BLOFIN_API_SECRET")
BLOFIN_API_PASSPHRASE = os.getenv("BLOFIN_API_PASSPHRASE")

def generate_signature(timestamp, method, request_path, body=""):
    pre_hash = f"{timestamp}{method}{request_path}{body}"
    print("🔑 Pre-hash string:", pre_hash)  # Useful for debugging
    return hmac.new(BLOFIN_API_SECRET.encode(), pre_hash.encode(), hashlib.sha256).hexdigest()

def get_price(symbol):
    request_path = f"/api/v1/futures/public/market/ticker?symbol={symbol}"
    url = BLOFIN_API_URL + request_path

    print(f"\n🔍 Fetching price for {symbol}...")
    print(f"Request URL: {url}")

    try:
        response = requests.get(url)  # No headers!
        response.raise_for_status()
        data = response.json()

        print(f"📦 API Response:\n{json.dumps(data, indent=2)}")

        if data.get("code") == "00000":
            return float(data["data"][0]["asks"][0][0])
        else:
            print(f"❌ Error fetching price: {data}")
            return None
    except Exception as e:
        print(f"❌ Exception fetching price: {e}")
        return None

def place_order(symbol, side, size, price=None, order_type="market"):
    method = "POST"
    request_path = "/api/v1/futures/v2/private/order/place"
    url = BLOFIN_API_URL + request_path
    timestamp = str(int(time.time() * 1000))

    body_data = {
        "instId": symbol,
        "tdMode": "cross",
        "side": side.lower(),  # Make sure it's "buy" or "sell"
        "ordType": order_type,
        "sz": str(size)
    }

    if price and order_type == "limit":
        body_data["px"] = str(price)

    body = json.dumps(body_data)
    signature = generate_signature(timestamp, method, request_path, body)

    headers = {
        "X-BLOFIN-API-KEY": BLOFIN_API_KEY,
        "X-BLOFIN-TIMESTAMP": timestamp,
        "X-BLOFIN-SIGNATURE": signature,
        "X-BLOFIN-PASSPHRASE": BLOFIN_API_PASSPHRASE,
        "Content-Type": "application/json"
    }

    print("\n🧾 DEBUG SIGNATURE BLOCK")
    print("Timestamp:", timestamp)
    print("Method:", method)
    print("Request Path:", request_path)
    print("Body:", body)
    print("Signature:", signature)

    try:
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        data = response.json()

        print("🔧 Response status:", response.status_code)
        print("🔧 Response data:", data)

        if data.get("code") == "00000":
            print(f"✅ Order successful for {symbol}: {data['data']}")
            return data["data"]
        else:
            print(f"❌ Order failed for {symbol}: {data}")
            return None
    except Exception as e:
        print(f"❌ Order exception for {symbol}: {e}")
        return None