import json
import os

PROFIT_FILE = "total_profit.json"

def load_total_profit():
    if not os.path.exists(PROFIT_FILE):
        return 0.0
    with open(PROFIT_FILE, "r") as f:
        return json.load(f).get("total_profit", 0.0)

def update_total_profit(pnl):
    total = load_total_profit() + pnl
    with open(PROFIT_FILE, "w") as f:
        json.dump({"total_profit": round(total, 2)}, f)
    return total