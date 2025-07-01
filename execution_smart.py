import random

# Simulate slippage (e.g. 0.2% worse execution price)
def apply_slippage(entry_price, slippage_pct=0.002):
    return entry_price * (1 - slippage_pct if random.random() < 0.5 else 1 + slippage_pct)

# Simulate funding fees per trade (fixed or percentage)
def apply_funding_fee(amount, rate=0.0005):
    return -amount * rate  # negative = cost

# Simulate order execution success/failure
def simulate_order_success(failure_rate=0.02):
    return random.random() > failure_rate  # 98% chance success

# Full wrapper to simulate a trade result
def simulate_trade_result(entry_price, direction, amount):
    slippage_price = apply_slippage(entry_price)
    pnl_change = random.uniform(-0.03, 0.05)  # -3% to +5% move

    if direction == "buy":
        pnl = (slippage_price * (1 + pnl_change)) - slippage_price
    else:
        pnl = slippage_price - (slippage_price * (1 - pnl_change))

    funding_cost = apply_funding_fee(amount)
    return (pnl * amount) + funding_cost  # Net PnL