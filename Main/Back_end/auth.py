from Back_end.storage import get_connection


def authenticate_user(email: str, password: str):
    """
    Looks up the user in SQLite by email + password.

    Returns:
      {"email": "...", "role": "applicant|caseworker"} if valid
      None if invalid
    """
    email_clean = (email or "").strip().lower()
    password_clean = password or ""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT email, role
        FROM users
        WHERE lower(email) = ? AND password = ?
    """, (email_clean, password_clean))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "email": row[0],
            "role": (row[1] or "").strip().lower()
        }

    return None