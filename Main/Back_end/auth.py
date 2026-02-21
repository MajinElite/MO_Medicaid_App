# Back_end/auth.py
import json
import os

def _db_path():
    # Main/Data/database.json (relative to this file)
    base_dir = os.path.dirname(os.path.dirname(__file__))  # goes to Main/
    return os.path.join(base_dir, "Data", "database.json")

def load_database():
    path = _db_path()

    if not os.path.exists(path):
        # If the file is missing, treat as empty db
        return {"users": [], "applications": []}

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Ensure keys exist
    if "users" not in data:
        data["users"] = []
    if "applications" not in data:
        data["applications"] = []

    return data

def authenticate_user(email: str, password: str):
    """
    Looks up the user in database.json by email + password.

    Returns:
      {"email": "...", "role": "applicant|caseworker"} if valid
      None if invalid
    """
    db = load_database()

    email_clean = (email or "").strip().lower()
    password_clean = password or ""

    for user in db.get("users", []):
        user_email = (user.get("email") or "").strip().lower()
        user_pass = user.get("password") or ""
        user_role = (user.get("role") or "").strip().lower()

        if user_email == email_clean and user_pass == password_clean:
            return {
                "email": user.get("email"),
                "role": user_role
            }

    return None