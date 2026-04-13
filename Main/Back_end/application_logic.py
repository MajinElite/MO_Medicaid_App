from datetime import datetime
import uuid

from Back_end.storage import get_connection


# ================= TIME HELPERS =================

def _now_iso():
    return datetime.now().isoformat(timespec="seconds")


def _make_app_id():
    return uuid.uuid4().hex[:8].upper()


# ================= ROW → DICT =================

def _row_to_application(row):
    if not row:
        return None

    return {
        "app_id": row[1],
        "applicant_email": row[2],
        "status": row[3],
        "deny_reason": row[4] or "",
        "created_at": row[5],
        "updated_at": row[6],

        "form": {
            "applicant_name": row[7] or "",
            "employer_name": row[8] or "",
            "employee_id": row[9] or "",
            "employment_status": row[10] or "",
            "start_date": row[11] or "",
            "hours_per_week": row[12] or "",
            "monthly_income": row[13] or "",
            "document_name": row[14] or "",
            "document_data_base64": row[15] or "",
            "additional_information": row[16] or "",

            # NEW
            "exemption_requested": row[17] or "No",
            "exemption_reason": row[18] or "",

            "request_file_name": row[19] or "",
            "request_file_data_base64": row[20] or ""
        }
    }


# ================= FIND APPLICATION =================

def find_application_by_email(email: str):
    email_clean = (email or "").strip().lower()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM applications
        WHERE lower(applicant_email) = ?
        ORDER BY id DESC
        LIMIT 1
    """, (email_clean,))

    row = cursor.fetchone()
    conn.close()

    return _row_to_application(row)


# ================= SUBMIT =================

def submit_employment_verification(user: dict, payload: dict):
    email = (user.get("email") or "").strip().lower()
    if not email:
        return False

    now = _now_iso()
    app_id = _make_app_id()

    conn = get_connection()
    cursor = conn.cursor()

    # Replace existing application
    cursor.execute("""
        DELETE FROM applications
        WHERE lower(applicant_email) = ?
    """, (email,))

    cursor.execute("""
        INSERT INTO applications (
            app_id,
            applicant_email,
            status,
            deny_reason,
            created_at,
            updated_at,
            applicant_name,
            employer_name,
            employee_id,
            employment_status,
            start_date,
            hours_per_week,
            monthly_income,
            document_name,
            document_data_base64,
            additional_information,
            exemption_requested,
            exemption_reason
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        app_id,
        email,
        "Pending",
        "",
        now,
        now,
        payload.get("applicant_name", ""),
        payload.get("employer_name", ""),
        payload.get("employee_id", ""),
        payload.get("employment_status", ""),
        payload.get("start_date", ""),
        payload.get("hours_per_week", ""),
        payload.get("monthly_income", ""),
        payload.get("document_name", ""),
        payload.get("document_data_base64", ""),
        payload.get("additional_information", ""),
        payload.get("exemption_requested", "No"),
        payload.get("exemption_reason", "")
    ))

    conn.commit()
    conn.close()
    return True


# ================= STATUS =================

def get_application_status(user: dict):
    email = (user.get("email") or "").strip().lower()

    app = find_application_by_email(email)
    if not app:
        return {"status": "None", "reason": ""}

    return {
        "status": app.get("status", "Pending"),
        "reason": app.get("deny_reason", ""),
        "request_file_name": app["form"].get("request_file_name", ""),
        "request_file_data_base64": app["form"].get("request_file_data_base64", "")
    }


# ================= GET ALL =================

def get_all_applications():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications ORDER BY created_at DESC")

    rows = cursor.fetchall()
    conn.close()

    return [_row_to_application(row) for row in rows]


# ================= APPROVE =================

def approve_application(app_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET status = ?, deny_reason = ?, updated_at = ?
        WHERE app_id = ?
    """, ("Approved", "", _now_iso(), app_id))

    conn.commit()
    conn.close()
    return True


# ================= DENY =================

def deny_application(app_id: str, reason: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET status = ?, deny_reason = ?, updated_at = ?
        WHERE app_id = ?
    """, ("Denied", reason.strip(), _now_iso(), app_id))

    conn.commit()
    conn.close()
    return True


# ================= REQUEST MORE INFO =================

def request_more_info(app_id: str, reason: str, file_name="", file_data=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET status = ?,
            deny_reason = ?,
            request_file_name = ?,
            request_file_data_base64 = ?,
            updated_at = ?
        WHERE app_id = ?
    """, (
        "More Info Required",
        reason.strip(),
        file_name,
        file_data,
        _now_iso(),
        app_id
    ))

    conn.commit()
    conn.close()
    return True