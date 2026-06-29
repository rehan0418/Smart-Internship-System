import sqlite3

conn = sqlite3.connect("internship.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM students")

conn.commit()
conn.close()

print("All Student Records Deleted")