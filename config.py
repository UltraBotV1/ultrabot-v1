# config.py

# Trading pairs supported for Futures (BloFin uses dash, not USDT concatenation)
TOKEN_LIST = [
    "BTC-USDT",
    "ETH-USDT",
    "SOL-USDT",
    "XRP-USDT",
    "DOGE-USDT",
    "ADA-USDT",
    "DOT-USDT",
    "LTC-USDT",
    "LINK-USDT",
    "ONDO-USDT",
    "TAO-USDT"
]

# Interval in seconds (15 minutes = 900 seconds)
TRADE_INTERVAL = 900

# Risk management (customize as needed)
MAX_TRADE_SIZE = 100  # max USDT per trade
STOP_LOSS_PERCENT = 5  # stop loss trigger
TAKE_PROFIT_PERCENT = 15  # take profit trigger

# Telegram alerts
ENABLE_TELEGRAM_ALERTS = True