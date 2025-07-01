import time
from blofin_api import get_price, place_order
from telegram_utils import send_telegram_message

# ✅ Token List
TOKEN_LIST = [
    "BTC-USDT", "ETH-USDT", "SOL-USDT", "XRP-USDT", "DOGE-USDT", "ADA-USDT", 
    "DOT-USDT", "LTC-USDT", "LINK-USDT", "ONDO-USDT", "TAO-USDT"
]

# ✅ Trading Config
TRADE_AMOUNT = 10
LEVERAGE = 5
MAX_RETRIES = 3

def analyze_and_trade():
    for token in TOKEN_LIST:
        try:
            print(f"\n🔍 Analyzing {token}...")
            price = None

            # Retry price fetch
            for attempt in range(MAX_RETRIES):
                price = get_price(token)
                if price:
                    break
                else:
                    print(f"❌ Failed to fetch price for {token}, retrying...")
                    time.sleep(2)

            if not price:
                print(f"❌ Failed to fetch price for {token} after {MAX_RETRIES} attempts.")
                continue

            print(f"✅ {token} price: {price}")
            send_telegram_message(f"✅ {token} price: {price}")

            # ✅ Sample Trade Logic
            side = "BUY"
            quantity = TRADE_AMOUNT
            print(f"📈 Placing {side} order for {token} amount {quantity}...")
            result = place_order(token, side, quantity)

            if result:
                print(f"✅ Order result: {result}")
                send_telegram_message(f"✅ Order placed for {token}: {result}")
            else:
                print(f"⚠️ Order failed for {token}")
                send_telegram_message(f"⚠️ Order failed for {token}")

        except Exception as e:
            print(f"🔥 Error during trade logic for {token}: {e}")

def main():
    while True:
        print("\n🟢 Starting new trading cycle...")
        analyze_and_trade()
        print("⏱ Sleeping 15 minutes...\n")
        time.sleep(900)

if __name__ == "__main__":
    main()