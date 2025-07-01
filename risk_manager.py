import os
import json
from datetime import datetime

RISK_FILE = "daily_risk.json"
MAX_DAILY_LOSS = 200  # <-- Customize your daily max loss ($)
STOP_LOSS_PERCENT = 0.10  # Stop-loss at 10% loss
TRAILING_STOP_PERCENT = 0.15  # Trail profits if up > 15%

def load_daily_risk():
    if not os.path.exists(RISK_FILE):
        return {"date": today_str(), "loss": 0}
    with open(RISK_FILE, "r") as f:
        return json.load(f)

def save_daily_risk(data):
    with open(RISK_FILE, "w") as f:
        json.dump(data, f)

def today_str():
    return datetime.now().strftime("%Y-%m-%d")

def should_stop_trading(result):
    data = load_daily_risk()
    if data["date"] != today_str():
        data = {"date": today_str(), "loss": 0}  # Reset new day

    if result < 0:
        data["loss"] += abs(result)

    save_daily_risk(data)
    return data["loss"] >= MAX_DAILY_LOSS

def apply_stop_loss(entry_price, current_price):
    loss_percent = (entry_price - current_price) / entry_price
    return loss_percent >= STOP_LOSS_PERCENT

def apply_trailing_stop(entry_price, current_price, highest_price):
    gain_percent = (highest_price - entry_price) / entry_price
    drop_percent = (highest_price - current_price) / highest_price
    return gain_percent >= TRAILING_STOP_PERCENT and drop_percent >= 0.05