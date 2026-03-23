import json
import os
from datetime import datetime

HISTORY_FILE = "data/history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_scan(url, patterns):
    history = load_history()
    if url not in history:
        history[url] = []
    history[url].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_patterns": len(patterns),
        "high":   sum(1 for p in patterns if p.get("severity") == "High"),
        "medium": sum(1 for p in patterns if p.get("severity") == "Medium"),
        "low":    sum(1 for p in patterns if p.get("severity") == "Low"),
        "patterns": patterns
    })
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_url_history(url):
    history = load_history()
    return history.get(url, [])

def get_all_tracked_urls():
    history = load_history()
    return list(history.keys())