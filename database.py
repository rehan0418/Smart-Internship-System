import sqlite3

conn = sqlite3.connect("internship.db")
cursor = conn.cursor()

# ==========================
# Students Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    department TEXT,
    attendance INTEGER DEFAULT 0,
    tasks_completed INTEGER DEFAULT 0,
    rating INTEGER DEFAULT 0
)
""")

# ==========================
# Tasks Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    task_title TEXT,
    task_description TEXT,
    status TEXT
)
""")

# ==========================
# Mentors Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS mentors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# ==========================
# Feedback Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    feedback TEXT
)
""")

# ==========================
# Location Attendance Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS location_attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    latitude TEXT,
    longitude TEXT,
    attendance_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS selfie_attendance(
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_name TEXT,
image_path TEXT,
date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
role TEXT
)
""")
conn.commit()
conn.close()

print("Database Created Successfully")