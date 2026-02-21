# Back_end/application_logic.py
from datetime import datetime
import uuid

from Back_end.storage import load_db, save_db

def _now_iso():
    return datetime.now().isoformat(timespec="seconds")

def _make_app_id():
    return uuid.uuid4().hex[:8].upper()

def find_application_by_email(email: str):
    db = load_db()
    email_clean = (email or "").strip().lower()

    for app in db.get("applications", []):
        if (app.get("applicant_email") or "").strip().lower() == email_clean:
            return app

    return None

def submit_employment_verification(user: dict, payload: dict):
    """
    Creates or overwrites an applicant's application and sets status to Pending.
    This is what makes Status show Under Review on applicant side.
    """
    db = load_db()
    email = (user.get("email") or "").strip().lower()
    if not email:
        return False

    new_app = {
        "app_id": _make_app_id(),
        "applicant_email": email,
        "status": "Pending",            # Pending = not reviewed yet
        "deny_reason": "",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),

        # store the submitted form fields
        "form": {
            "applicant_name": payload.get("applicant_name", ""),
            "employer_name": payload.get("employer_name", ""),
            "employee_id": payload.get("employee_id", ""),
            "employment_status": payload.get("employment_status", ""),
            "start_date": payload.get("start_date", ""),
            "hours_per_week": payload.get("hours_per_week", ""),
            "document_name": payload.get("document_name", "")
        }
    }

    # remove any old application for this email (so only 1 exists per applicant)
    db["applications"] = [
        a for a in db.get("applications", [])
        if (a.get("applicant_email") or "").strip().lower() != email
    ]

    db["applications"].append(new_app)
    save_db(db)
    return True

def get_application_status(user: dict):
    """
    Returns dict:
      {"status": "None|Pending|Approved|Denied", "reason": "..."}
    """
    email = (user.get("email") or "").strip().lower()
    if not email:
        return {"status": "None", "reason": ""}

    app = find_application_by_email(email)
    if not app:
        return {"status": "None", "reason": ""}

    return {
        "status": app.get("status", "Pending"),
        "reason": app.get("deny_reason", "")
    }

def get_all_applications():
    """
    Returns list of apps for caseworker table.
    """
    db = load_db()
    return db.get("applications", [])

def approve_application(app_id: str):
    db = load_db()
    for app in db.get("applications", []):
        if app.get("app_id") == app_id:
            app["status"] = "Approved"
            app["deny_reason"] = ""
            app["updated_at"] = _now_iso()
            save_db(db)
            return True
    return False

def deny_application(app_id: str, reason: str):
    db = load_db()
    for app in db.get("applications", []):
        if app.get("app_id") == app_id:
            app["status"] = "Denied"
            app["deny_reason"] = reason.strip()
            app["updated_at"] = _now_iso()
            save_db(db)
            return True
    return False