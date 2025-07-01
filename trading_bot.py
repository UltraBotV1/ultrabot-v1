import time
from datetime import datetime
from blofin_api import get_price, place_order, get_balance
from strategy import evaluate_trade_setup
from trade_logger import log_trade
from telegram_alerts import send_telegram_message
from utils import load_trade_history, save_trade_history

# === CONFIG ===
SYMBOLS = [
    "BTC-USDT", "ETH-USDT", "SOL-USDT", "XRP-USDT", "DOGE-USDT", "ADA-USDT",
    "DOT-USDT", "LTC-USDT", "LINK-USDT", "ONDO-USDT", "TAO-USDT"
]
TRADE_INTERVAL = 15 * 60  # 15 minutes in seconds
POSITION_SIZE_PERCENT = 0.10  # Use 10% of available USDT per trade
LEVERAGE = 10
MAX_TRADE_HISTORY = 100

# === MAIN LOOP ===
def run_bot():
    print("🔁 Starting 15-minute trading bot...")
    trade_history = load_trade_history()

    while True:
        for symbol in SYMBOLS:
            print(f"\n🧠 Analyzing {symbol}...")
            price = get_price(symbol)

            if price is None:
                print(f"⚠️ Skipping {symbol} due to price fetch error.")
                continue

            prices = [price] * 200  # Replace with historical prices fetch in future
            signal = evaluate_trade_setup(prices)

            if signal:
                print(f"📢 Trade Signal: {signal} on {symbol} at {price}")
                balance = get_balance("USDT")
                trade_amount = round(balance * POSITION_SIZE_PERCENT, 2)

                order_response = place_order(
                    symbol=symbol,
                    side="buy" if signal == "LONG" else "sell",
                    amount=trade_amount,
                    leverage=LEVERAGE
                )

                if order_response.get("code") == "00000":
                    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    log_msg = f"{timestamp} | {symbol} | {signal} | Entry: {price} | Size: {trade_amount} USDT"
                    log_trade(log_msg)
                    send_telegram_message(f"✅ {log_msg}")
                    trade_history.append(log_msg)

                    if len(trade_history) > MAX_TRADE_HISTORY:
                        trade_history = trade_history[-MAX_TRADE_HISTORY:]

                    save_trade_history(trade_history)
                else:
                    print(f"❌ Order failed: {order_response}")
            else:
                print(f"⚠️ No trade setup detected for {symbol}")

        print("⏳ Waiting 15 minutes until next cycle...\n")
        time.sleep(TRADE_INTERVAL)

if __name__ == "__main__":
    run_bot()