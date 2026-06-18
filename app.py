from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -----------------------
# Login Pages
# -----------------------

# Home Page
@app.route('/')
def home():
    return render_template("login.html")

# Student Login Page
@app.route('/student_login')
def student_login():
    return render_template("student_login.html")

# Mentor Login Page
@app.route('/mentor')
def mentor():
    return render_template("mentor_login.html")



@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# -----------------------
# Student Registration
# -----------------------

@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/save_student', methods=['POST'])
def save_student():

    name = request.form['name']
    email = request.form['email']
    department = request.form['department']

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (name,email,department)
    VALUES(?,?,?)
    """, (name, email, department))

    conn.commit()
    conn.close()

    return redirect('/dashboard')


# -----------------------
# Task Module
# -----------------------

@app.route('/task')
def task():
    return render_template("task.html")


@app.route('/save_task', methods=['POST'])
def save_task():

    student_name = request.form['student_name']
    task_title = request.form['task_title']
    task_description = request.form['task_description']
    status = request.form['status']

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks
    (student_name, task_title, task_description, status)
    VALUES(?,?,?,?)
    """,
    (student_name,
     task_title,
     task_description,
     status))

    conn.commit()
    conn.close()

    return redirect('/tasks')


@app.route('/tasks')
def tasks():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "tasks.html",
        tasks=data
    )


# -----------------------
# Attendance Module
# -----------------------

@app.route('/attendance')
def attendance():
    return render_template("attendance.html")


@app.route('/save_attendance', methods=['POST'])
def save_attendance():

    student_name = request.form['student_name']
    attendance = int(request.form['attendance'])

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students
    SET attendance = attendance + ?
    WHERE name = ?
    """, (attendance, student_name))

    conn.commit()
    conn.close()

    return redirect('/dashboard')


# -----------------------
# Ranking Module
# -----------------------

@app.route('/ranking')
def ranking():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM students
    ORDER BY rating DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "ranking.html",
        students=data
    )


# -----------------------
# Rating Update
# -----------------------

@app.route('/update_rating/<int:id>/<int:rating>')
def update_rating(id, rating):

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET rating=? WHERE id=?",
        (rating, id)
    )

    conn.commit()
    conn.close()

    return redirect('/ranking')


# -----------------------
# Report Module
# -----------------------

@app.route('/report')
def report():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "report.html",
        students=data
    )


# -----------------------
# Certificate Eligibility
# -----------------------

@app.route('/certificate')
def certificate():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "certificate.html",
        students=data
    )
@app.route('/student_dashboard')
def student_dashboard():
    return render_template("student_dashboard.html")


@app.route('/mentor_dashboard')
def mentor_dashboard():
    return render_template("mentor_dashboard.html")
@app.route('/rating')
def rating():
    return render_template("rating.html")


@app.route('/save_rating', methods=['POST'])
def save_rating():

    student_name = request.form['student_name']
    rating = request.form['rating']

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students
    SET rating=?
    WHERE name=?
    """, (rating, student_name))

    conn.commit()
    conn.close()

    return redirect('/ranking')
@app.route('/students')
def students():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=data
    )
@app.route('/view_attendance')
def view_attendance():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "view_attendance.html",
        students=data
    )
@app.route('/view_rating')
def view_rating():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "view_rating.html",
        students=data
    )


# -----------------------
# Run App
# -----------------------

if __name__ == "__main__":
    app.run(debug=True)