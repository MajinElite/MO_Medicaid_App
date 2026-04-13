from storage import get_connection, init_db

init_db()

conn = get_connection()
cursor = conn.cursor()

# Insert users (same as your JSON)
cursor.execute("""
INSERT OR IGNORE INTO users (email, password, role)
VALUES (?, ?, ?)
""", ("applicant1@gmail.com", "12345", "applicant"))

cursor.execute("""
INSERT OR IGNORE INTO users (email, password, role)
VALUES (?, ?, ?)
""", ("caseworker1@gmail.com", "abcd", "caseworker"))

conn.commit()
conn.close()

print("Users added successfully.")