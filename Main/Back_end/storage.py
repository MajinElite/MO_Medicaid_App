# Back_end/storage.py
import json
import os

def _db_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Main/
    return os.path.join(base_dir, "Data", "database.json")

def load_db():
    path = _db_path()

    if not os.path.exists(path):
        return {"users": [], "applications": []}

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "users" not in data:
        data["users"] = []
    if "applications" not in data:
        data["applications"] = []

    return data

def save_db(data: dict):
    path = _db_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)