import json
from datetime import datetime, timedelta
import os

# Initial allocation (can be loaded from a file too)
balance = {
    "main": 700.0,
    "sniper": 300.0
}

profit_log_path = "profit_log.json"
balance_file = "balance.json"

# Load previous balance if exists
if os.path.exists(balance_file):
    with open(balance_file, "r") as f:
        balance = json.load(f)

# Load profit log
if os.path.exists(profit_log_path):
    with open(profit_log_path, "r") as f:
        profit_log = json.load(f)
else:
    profit_log = {
        "main": [],
        "sniper": []
    }

def update_profit(strategy, amount):
    """Log profit/loss for a strategy"""
    profit_log[strategy].append({
        "timestamp": datetime.utcnow().isoformat(),
        "amount": round(amount, 2)
    })
    with open(profit_log_path, "w") as f:
        json.dump(profit_log, f, indent=2)

def get_available_balance(strategy):
    return balance.get(strategy, 0)

def deduct_from_balance(strategy, amount):
    balance[strategy] = max(0, balance[strategy] - amount)
    save_balance()

def add_to_balance(strategy, amount):
    balance[strategy] += amount
    save_balance()

def save_balance():
    with open(balance_file, "w") as f:
        json.dump(balance, f, indent=2)

def compound_daily_profits():
    """Reinvest all profits once per day"""
    today = datetime.utcnow().date()
    compounded = {"main": 0, "sniper": 0}

    for strategy in ["main", "sniper"]:
        total = 0
        # Keep only logs from today
        updated_log = []
        for entry in profit_log[strategy]:
            ts = datetime.fromisoformat(entry["timestamp"])
            if ts.date() == today:
                total += entry["amount"]
            else:
                updated_log.append(entry)
        if total != 0:
            balance[strategy] += round(total, 2)
            compounded[strategy] = round(total, 2)
        profit_log[strategy] = updated_log

    save_balance()

    with open(profit_log_path, "w") as f:
        json.dump(profit_log, f, indent=2)

    return compounded

def print_balance():
    print(f"\n💰 Current Balances:")
    for k, v in balance.items():
        print(f"   - {k.capitalize()} Bot: ${v:.2f}")

# ✅ Risk management: daily loss cap
MAX_DAILY_LOSS = -100  # Adjust to your risk tolerance

def should_stop_trading(profit):
    """
    Halts trading if cumulative profit is below max daily loss.
    """
    try:
        with open("daily_profit.txt", "r") as f:
            daily_profit = float(f.read())
    except:
        daily_profit = 0

    daily_profit += profit

    with open("daily_profit.txt", "w") as f:
        f.write(str(daily_profit))

    return daily_profit < MAX_DAILY_LOSS