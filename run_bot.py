import time
from main import analyze_and_trade

INTERVAL_MINUTES = 15

if __name__ == "__main__":
    print("🚀 Crypto Futures Bot started. Trading every 15 minutes.")
    while True:
        try:
            analyze_and_trade()
        except Exception as e:
            print(f"⚠️ Bot error: {e}")
        print(f"⏳ Waiting {INTERVAL_MINUTES} minutes until next trade...")
        time.sleep(INTERVAL_MINUTES * 60)