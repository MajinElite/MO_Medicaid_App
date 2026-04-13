from storage import get_connection, init_db

conn = get_connection()
cursor = conn.cursor()

cursor.execute("DELETE FROM applications")

conn.commit()
conn.close()

print("Applications cleared.")