import random

def place_order(token, side, quantity, profit=None):
    """
    Simulated order placement logic.
    """
    print(f"📥 Executing {side.upper()} order for {token} | Qty: {quantity}")

    # Simulate profit outcome
    profit = round(random.uniform(-5, 15), 2)
    return True, profit

def close_trade(token):
    """
    Optional: Add logic to close a trade here.
    """
    print(f"🔻 Closing position for {token}")
    return True

def simulate_price_movement(entry_price, direction="up"):
    """
    Simulates market price movement based on direction.
    """
    if direction == "up":
        return round(entry_price * random.uniform(1.01, 1.10), 4)
    elif direction == "down":
        return round(entry_price * random.uniform(0.90, 0.99), 4)
    else:
        return entry_price

def get_current_price(token):
    """
    Dummy price fetcher (replace with real exchange API call).
    """
    price = round(random.uniform(0.75, 1.25), 4)
    print(f"💰 Current price for {token}: {price}")
    return price

def apply_stop_loss(entry_price, current_price, threshold=0.9):
    """
    Returns True if current price is below stop-loss threshold.
    """
    return current_price < entry_price * threshold

def calculate_dynamic_quantity(token, balance, price):
    """
    Calculate how much to buy based on balance and price.
    Replace with logic using live balance and price data.
    """
    allocation = 0.05  # 5% of balance per trade
    quantity = round((balance * allocation) / price, 2)
    return quantity