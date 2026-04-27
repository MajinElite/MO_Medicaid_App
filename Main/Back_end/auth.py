from Back_end.storage import get_connection


def authenticate_user(email: str, password: str):
    """
    Authenticates user from database.

    Returns:
        {
            "email": "...",
            "role": "applicant|caseworker|admin",
            "status": "active|locked"
        }
    OR
        None if invalid or locked
    """

    email_clean = (email or "").strip().lower()
    password_clean = password or ""

    conn = get_connection()
    cursor = conn.cursor()

    # 🔥 Updated query (includes status)
    cursor.execute("""
        SELECT email, role, status
        FROM users
        WHERE lower(email) = ? AND password = ?
    """, (email_clean, password_clean))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    email_db, role_db, status_db = row

    role = (role_db or "").strip().lower()
    status = (status_db or "active").strip().lower()

    # 🔒 Block locked users
    if status == "locked":
        return {
            "email": email_db,
            "role": role,
            "status": "locked"
        }

    return {
        "email": email_db,
        "role": role,
        "status": status
    }