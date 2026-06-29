import sqlite3

conn = sqlite3.connect("internship.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM tasks")
cursor.execute("DELETE FROM feedback")
cursor.execute("DELETE FROM location_attendance")
cursor.execute("DELETE FROM selfie_attendance")

conn.commit()
conn.close()

print("All data deleted successfully")