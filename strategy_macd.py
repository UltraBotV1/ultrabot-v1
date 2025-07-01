def is_macd_bullish(macd_line, signal_line):
    """
    Returns True if MACD line crosses above the signal line.
    """
    return macd_line > signal_line

def is_macd_bearish(macd_line, signal_line):
    """
    Returns True if MACD line crosses below the signal line.
    """
    return macd_line < signal_line

def get_macd_data(token):
    """
    Placeholder function for MACD values. Replace with real logic.
    """
    # Replace this with actual MACD calculation from price data
    mock_macd = 1.05
    mock_signal = 1.0
    return mock_macd, mock_signal