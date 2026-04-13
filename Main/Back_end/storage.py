import sqlite3
import os


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
        role TEXT NOT NULL
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

        -- NEW: EXEMPTION SYSTEM
        exemption_requested TEXT DEFAULT 'No',
        exemption_reason TEXT,

        -- NEW: REQUEST MORE INFO FILE SUPPORT
        request_file_name TEXT,
        request_file_data_base64 TEXT
    )
    """)

    # ================= SAFE MIGRATION (VERY IMPORTANT) =================
    # This adds new columns if your DB already exists

    def add_column_if_missing(column_name, column_def):
        cursor.execute("PRAGMA table_info(applications)")
        columns = [col[1] for col in cursor.fetchall()]

        if column_name not in columns:
            cursor.execute(f"ALTER TABLE applications ADD COLUMN {column_name} {column_def}")

    # Exemption columns
    add_column_if_missing("exemption_requested", "TEXT DEFAULT 'No'")
    add_column_if_missing("exemption_reason", "TEXT")

    # Request more info file columns
    add_column_if_missing("request_file_name", "TEXT")
    add_column_if_missing("request_file_data_base64", "TEXT")

    conn.commit()
    conn.close()