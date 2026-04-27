import sqlite3
import os
from datetime import datetime


def _db_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Main/
    return os.path.join(base_dir, "Data", "database.db")


def get_connection():
    return sqlite3.connect(_db_path())


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ================= USERS TABLE =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT,
        updated_at TEXT
    )
    """)

    # ================= APPLICATIONS TABLE =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_id TEXT UNIQUE NOT NULL,
        applicant_email TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending',
        deny_reason TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,

        applicant_name TEXT,
        employer_name TEXT,
        employee_id TEXT,
        employment_status TEXT,
        start_date TEXT,
        hours_per_week TEXT,
        monthly_income TEXT,
        document_name TEXT,
        document_data_base64 TEXT,
        additional_information TEXT,

        exemption_requested TEXT DEFAULT 'No',
        exemption_reason TEXT,

        request_file_name TEXT,
        request_file_data_base64 TEXT
    )
    """)

    # ================= SAFE MIGRATIONS =================
    def add_column_if_missing(table_name, column_name, column_def):
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        if column_name not in columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_def}")

    # Users migrations
    add_column_if_missing("users", "status", "TEXT NOT NULL DEFAULT 'active'")
    add_column_if_missing("users", "created_at", "TEXT")
    add_column_if_missing("users", "updated_at", "TEXT")

    # Applications migrations
    add_column_if_missing("applications", "exemption_requested", "TEXT DEFAULT 'No'")
    add_column_if_missing("applications", "exemption_reason", "TEXT")
    add_column_if_missing("applications", "request_file_name", "TEXT")
    add_column_if_missing("applications", "request_file_data_base64", "TEXT")

    now = datetime.now().isoformat(timespec="seconds")

    # ================= DEFAULT ADMIN ACCOUNT =================
    cursor.execute("""
        INSERT OR IGNORE INTO users (email, password, role, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "admin@example.com",
        "admin123",
        "admin",
        "active",
        now,
        now
    ))

    # ================= DUMMY DEMO USERS =================
    dummy_users = [
        ("frank@example.com", "pass123", "applicant"),
        ("lisa@example.com", "pass123", "applicant"),
        ("john@example.com", "pass123", "applicant"),
        ("emma@example.com", "pass123", "applicant"),
        ("maria@example.com", "pass123", "applicant"),
        ("david@example.com", "pass123", "applicant"),
        ("bob@example.com", "pass123", "caseworker"),
        ("sarah@example.com", "pass123", "caseworker"),
    ]

    for email, password, role in dummy_users:
        cursor.execute("""
            INSERT OR IGNORE INTO users (email, password, role, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            email,
            password,
            role,
            "active",
            now,
            now
        ))

    conn.commit()
    conn.close()


# ================= USER MANAGEMENT FUNCTIONS =================

def get_all_managed_users():
    """
    Returns all non-admin users for the Admin User Management screen.
    Admin accounts are intentionally hidden.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, email, role, status, created_at, updated_at
        FROM users
        WHERE lower(role) != 'admin'
        ORDER BY role, email
    """)

    rows = cursor.fetchall()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "email": row[1],
            "role": row[2],
            "status": row[3],
            "created_at": row[4],
            "updated_at": row[5],
        })

    return users


def create_user(email, password, role):
    email = (email or "").strip().lower()
    password = password or ""
    role = (role or "").strip().lower()
    now = datetime.now().isoformat(timespec="seconds")

    if not email or not password or role not in ["applicant", "caseworker"]:
        return False, "Email, password, and valid role are required."

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (email, password, role, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            email,
            password,
            role,
            "active",
            now,
            now
        ))

        conn.commit()
        conn.close()

        return True, "User created successfully."

    except sqlite3.IntegrityError:
        return False, "A user with this email already exists."

    except Exception as e:
        return False, str(e)


def update_user(user_id, email, password, role):
    email = (email or "").strip().lower()
    password = password or ""
    role = (role or "").strip().lower()
    now = datetime.now().isoformat(timespec="seconds")

    if not user_id:
        return False, "Missing user ID."

    if not email or role not in ["applicant", "caseworker"]:
        return False, "Email and valid role are required."

    try:
        conn = get_connection()
        cursor = conn.cursor()

        if password:
            cursor.execute("""
                UPDATE users
                SET email = ?, password = ?, role = ?, updated_at = ?
                WHERE id = ? AND lower(role) != 'admin'
            """, (
                email,
                password,
                role,
                now,
                user_id
            ))
        else:
            cursor.execute("""
                UPDATE users
                SET email = ?, role = ?, updated_at = ?
                WHERE id = ? AND lower(role) != 'admin'
            """, (
                email,
                role,
                now,
                user_id
            ))

        conn.commit()
        changed = cursor.rowcount
        conn.close()

        if changed == 0:
            return False, "User could not be updated."

        return True, "User updated successfully."

    except sqlite3.IntegrityError:
        return False, "A user with this email already exists."

    except Exception as e:
        return False, str(e)


def delete_user(user_id):
    if not user_id:
        return False, "Missing user ID."

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM users
            WHERE id = ? AND lower(role) != 'admin'
        """, (user_id,))

        conn.commit()
        changed = cursor.rowcount
        conn.close()

        if changed == 0:
            return False, "User could not be deleted."

        return True, "User deleted successfully."

    except Exception as e:
        return False, str(e)


def lock_user(user_id):
    return set_user_status(user_id, "locked")


def unlock_user(user_id):
    return set_user_status(user_id, "active")


def set_user_status(user_id, status):
    if not user_id:
        return False, "Missing user ID."

    if status not in ["active", "locked"]:
        return False, "Invalid user status."

    now = datetime.now().isoformat(timespec="seconds")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET status = ?, updated_at = ?
            WHERE id = ? AND lower(role) != 'admin'
        """, (
            status,
            now,
            user_id
        ))

        conn.commit()
        changed = cursor.rowcount
        conn.close()

        if changed == 0:
            return False, "User status could not be updated."

        return True, f"User status changed to {status}."

    except Exception as e:
        return False, str(e)