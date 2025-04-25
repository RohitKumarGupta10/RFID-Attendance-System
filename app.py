from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Database
def init_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT UNIQUE NOT NULL,
            uid TEXT UNIQUE NOT NULL  -- Added UID field for RFID
        )
    """)
    
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_urn TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (student_urn) REFERENCES students(roll)
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize database at start
init_db()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attendance.html')
def attendance():
    return render_template('attendance.html')

@app.route('/registration.html', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form.get('name')
        roll = request.form.get('roll')
        uid = request.form.get('uid')  # Get the UID (RFID)

        if name and roll and uid:
            conn = sqlite3.connect('attendance.db')
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO students (name, roll, uid) VALUES (?, ?, ?)", (name, roll, uid))
                conn.commit()
                flash(f"✅ Student {name} registered successfully!", 'success')
            except sqlite3.IntegrityError:
                flash("⚠️ Roll number or UID already exists!", 'error')
            conn.close()
            return redirect(url_for('index'))
        else:
            flash("⚠️ Name, roll number, and UID are required!", 'error')
            return redirect(url_for('register_student'))

    return render_template('registration.html')

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    uid = request.form.get('uid')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not uid:
        flash("⚠️ No UID received!", 'error')
        return redirect(url_for('attendance'))

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT roll FROM students WHERE uid = ?", (uid,))
    student_urn = cursor.fetchone()

    if student_urn:
        cursor.execute("INSERT INTO attendance (student_urn, status, timestamp) VALUES (?, 'Present', ?)", (student_urn[0], timestamp))
        conn.commit()
        flash(f"✅ Attendance marked for Roll Number: {student_urn[0]}", 'success')
    else:
        flash("⚠️ RFID not registered!", 'error')

    conn.close()
    return redirect(url_for('attendance'))

@app.route('/dashboard.html')
def dashboard():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT student_urn, status, timestamp FROM attendance ORDER BY timestamp DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
