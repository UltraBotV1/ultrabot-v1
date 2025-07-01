# trade_tracker.py

import datetime

LOG_FILE = "trade_log.txt"

def log_trade(symbol, side, size, price):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {side.upper()} {symbol} | Size: {size} @ {price}\n")
    print(f"📝 Logged trade for {symbol}")