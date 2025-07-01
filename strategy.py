from technical_indicators import calculate_ema, calculate_macd, calculate_rsi, detect_breakout

def evaluate_trade_setup(prices):
    if len(prices) < 200:
        return None  # Not enough data

    ema_200 = calculate_ema(prices, period=200)
    macd_line, signal_line = calculate_macd(prices)
    rsi = calculate_rsi(prices)
    breakout = detect_breakout(prices)

    if not all([ema_200, macd_line, signal_line, rsi]):
        return None  # Incomplete data

    # Long setup
    if prices[-1] > ema_200 and macd_line > signal_line and 40 < rsi < 70 and breakout:
        return "LONG"

    # Short setup
    if prices[-1] < ema_200 and macd_line < signal_line and 30 < rsi < 60 and not breakout:
        return "SHORT"

    return None