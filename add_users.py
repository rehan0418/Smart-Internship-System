import sqlite3

conn = sqlite3.connect("internship.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO users
(username,password,role)
VALUES
('student','123','student')
""")

cursor.execute("""
INSERT INTO users
(username,password,role)
VALUES
('mentor','123','mentor')
""")

conn.commit()
conn.close()

print("Users Added")