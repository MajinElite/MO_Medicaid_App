# Back_end/application_logic.py

from datetime import datetime
import uuid

from Back_end.storage import load_db, save_db


# ================= TIME HELPERS =================

def _now_iso():
    return datetime.now().isoformat(timespec="seconds")


def _make_app_id():
    return uuid.uuid4().hex[:8].upper()


# ================= FIND APPLICATION =================

def find_application_by_email(email: str):
    db = load_db()
    email_clean = (email or "").strip().lower()

    for app in db.get("applications", []):
        if (app.get("applicant_email") or "").strip().lower() == email_clean:
            return app

    return None


# ================= SUBMIT VERIFICATION =================

def submit_employment_verification(user: dict, payload: dict):
    """
    Creates or overwrites an applicant's application and sets status to Pending.
    """

    db = load_db()

    email = (user.get("email") or "").strip().lower()
    if not email:
        return False

    new_app = {
        "app_id": _make_app_id(),
        "applicant_email": email,
        "status": "Pending",
        "deny_reason": "",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),

        # Store form data properly
        "form": {
            "applicant_name": payload.get("applicant_name", ""),
            "employer_name": payload.get("employer_name", ""),
            "employee_id": payload.get("employee_id", ""),
            "employment_status": payload.get("employment_status", ""),
            "start_date": payload.get("start_date", ""),
            "hours_per_week": payload.get("hours_per_week", ""),
            "monthly_income": payload.get("monthly_income", ""),
            "document_name": payload.get("document_name", ""),
            "document_data_base64": payload.get("document_data_base64", ""),
            "additional_information": payload.get("additional_information", "")
        }
    }

    # Remove old application for this email
    db["applications"] = [
        a for a in db.get("applications", [])
        if (a.get("applicant_email") or "").strip().lower() != email
    ]

    db["applications"].append(new_app)

    save_db(db)
    return True


# ================= STATUS CHECK =================

def get_application_status(user: dict):
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


# ================= GET ALL =================

def get_all_applications():
    db = load_db()
    return db.get("applications", [])


# ================= APPROVE =================

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


# ================= DENY =================

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