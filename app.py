from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
import base64
import time

app = Flask(__name__)
app.secret_key = "smartinternship"
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# -----------------------
# Login Pages
# -----------------------

# Home Page

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

    if 'role' not in session:
        return redirect('/')

    if session['role'] != 'student':
        return "Access Denied"

    return render_template(
        "student_dashboard.html"
    )


@app.route('/mentor_dashboard')
def mentor_dashboard():

    if 'role' not in session:
        return redirect('/')

    if session['role'] != 'mentor':
        return "Access Denied"

    return render_template(
        "mentor_dashboard.html"
    )
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
@app.route('/progress')
def progress():

    tasks = 15
    attendance = 85
    rating = 4

    progress_percent = int(
        (attendance + (rating*20)) / 2
    )

    return render_template(
        "progress.html",
        tasks=tasks,
        attendance=attendance,
        rating=rating,
        progress=progress_percent
    )
@app.route('/feedback')
def feedback():
    return render_template("feedback.html")


@app.route('/save_feedback', methods=['POST'])
def save_feedback():

    student_name = request.form['student_name']
    feedback = request.form['feedback']

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO feedback
    (student_name, feedback)
    VALUES (?,?)
    """,
    (student_name, feedback))

    conn.commit()
    conn.close()

    return redirect('/view_feedback')


@app.route('/view_feedback')
def view_feedback():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM feedback")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "view_feedback.html",
        feedbacks=data
    )
from flask import send_file
from reportlab.pdfgen import canvas
from reportlab.lib import colors

@app.route('/generate_certificate', methods=['POST'])
def generate_certificate():

    student_name = request.form['student_name']

    pdf_file = "certificate.pdf"

    c = canvas.Canvas(pdf_file)

    # Border
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(5)
    c.rect(20,20,550,800)

    # Title
    c.setFont("Helvetica-Bold",28)
    c.drawCentredString(
        300,
        760,
        "CERTIFICATE OF INTERNSHIP"
    )

    # Subtitle
    c.setFont("Helvetica",16)

    c.drawCentredString(
        300,
        700,
        "This Certificate is Proudly Presented To"
    )

    # Student Name
    c.setFont("Helvetica-Bold",24)

    c.drawCentredString(
        300,
        640,
        student_name
    )

    c.line(150,620,450,620)

    # Content
    c.setFont("Helvetica",14)

    c.drawCentredString(
        300,
        560,
        "For Successfully Completing Internship"
    )

    c.drawCentredString(
        300,
        530,
        "Smart Internship Tracking & Performance"
    )

    c.drawCentredString(
        300,
        500,
        "Management System"
    )

    c.drawCentredString(
        300,
        450,
        "Duration : 4 Weeks"
    )

    c.drawCentredString(
        300,
        420,
        "Awarded On : 21 June 2026"
    )

    # Signature
    c.setFont("Helvetica-Bold",14)

    c.drawString(
        70,
        120,
        "Mentor Signature"
    )

    c.line(
        70,
        140,
        200,
        140
    )

    c.drawString(
        400,
        120,
        "Director"
    )

    c.line(
        380,
        140,
        520,
        140
    )

    c.save()

    return send_file(
        pdf_file,
        as_attachment=True
    )
@app.route('/upload')
def upload():
    return render_template("upload.html")


@app.route('/upload_file', methods=['POST'])
def upload_file():

    file = request.files['file']

    if file:

        filename = secure_filename(file.filename)

        file.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

        return "File Uploaded Successfully"

    return "Upload Failed"
@app.route('/location_attendance')
def location_attendance():
    return render_template(
        "location_attendance.html"
    )

@app.route('/view_location_attendance')
def view_location_attendance():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM location_attendance")

    data = cursor.fetchall()

    conn.close()

    return str(data)
@app.route('/mark_location_attendance', methods=['POST'])
def mark_location_attendance():

    student_name = request.form['student_name']
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO location_attendance
    (student_name, latitude, longitude)
    VALUES (?, ?, ?)
    """, (student_name, latitude, longitude))

    conn.commit()
    conn.close()

    return "Attendance Marked Successfully"

@app.route('/save_photo', methods=['POST'])
def save_photo():

    photo_data = request.form['photo']

    photo_data = photo_data.split(',')[1]

    image = base64.b64decode(photo_data)

    os.makedirs(
        "attendance_photos",
        exist_ok=True
    )

    filename = (
        "attendance_photos/"
        + str(int(time.time()))
        + ".png"
    )

    with open(filename, "wb") as f:
        f.write(image)

    return """
    Attendance Marked Successfully
    """
@app.route('/analytics')
def analytics():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks")
    tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM location_attendance")
    attendance = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(rating) FROM students")
    rating = cursor.fetchone()[0]

    if rating is None:
        rating = 0

    cursor.execute("""
    SELECT name
    FROM students
    ORDER BY rating DESC
    LIMIT 1
    """)

    result = cursor.fetchone()

    if result:
        top_student = result[0]
    else:
        top_student = "No Data"

    conn.close()

    return render_template(
        "analytics.html",
        students=students,
        tasks=tasks,
        attendance=attendance,
        rating=round(rating, 2),
        top_student=top_student
    )

@app.route('/view_uploaded_reports')
def view_uploaded_reports():
 return "Uploaded Reports"
import os
from flask import request, redirect

UPLOAD_FOLDER = "static/selfies"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/camera_attendance', methods=['GET', 'POST'])
def camera_attendance():

    if request.method == 'POST':
        student_name = request.form['student_name']
        image = request.files['image']

        filepath = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(filepath)

        conn = sqlite3.connect("internship.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO selfie_attendance (student_name, image_path)
        VALUES (?, ?)
        """, (student_name, filepath))

        conn.commit()
        conn.close()

        return "Selfie Attendance Marked Successfully"

    return render_template("camera_attendance.html")
@app.route('/view_selfie_attendance')
def view_selfie_attendance():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT student_name, image_path, date FROM selfie_attendance")
    data = cursor.fetchall()

    conn.close()

    return render_template("view_selfie.html", data=data)
@app.route('/')
def home():
    return render_template("login.html")
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT role
    FROM users
    WHERE username=?
    AND password=?
    """,(username,password))

    user = cursor.fetchone()

    conn.close()

    if user:

        session['username'] = username
        session['role'] = user[0]

        if user[0] == "student":
            return redirect('/student_dashboard')

        else:
            return redirect('/mentor_dashboard')

    return "Invalid Username or Password"
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')
@app.route('/certificate_form')
def certificate_form():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template(
        "certificate_form.html",
        students=students
    )
@app.route('/mentor_tasks')
def mentor_tasks():

    conn = sqlite3.connect("internship.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return render_template(
        "mentor_tasks.html",
        tasks=tasks
    )
# -----------------------
# Run App
# -----------------------

if __name__ == "__main__":
    app.run(debug=True)
 