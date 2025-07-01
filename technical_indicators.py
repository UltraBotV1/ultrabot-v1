import numpy as np

def calculate_ema(prices, period=200):
    if len(prices) < period:
        return None
    weights = np.exp(np.linspace(-1., 0., period))
    weights /= weights.sum()
    ema = np.convolve(prices, weights, mode='valid')
    return ema[-1]

def calculate_macd(prices, slow=26, fast=12, signal=9):
    if len(prices) < slow:
        return None, None
    exp1 = np.convolve(prices, np.exp(np.linspace(-1., 0., fast))[::-1], mode='valid')
    exp2 = np.convolve(prices, np.exp(np.linspace(-1., 0., slow))[::-1], mode='valid')
    macd_line = exp1[-len(exp2):] - exp2
    signal_line = np.convolve(macd_line, np.exp(np.linspace(-1., 0., signal))[::-1], mode='valid')
    return macd_line[-1], signal_line[-1]

def calculate_rsi(prices, period=14):
    if len(prices) < period:
        return None
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = 100. - 100. / (1. + rs)
    return rsi

def detect_breakout(prices):
    if len(prices) < 2:
        return False
    recent_high = max(prices[:-1])
    return prices[-1] > recent_high