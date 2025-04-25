from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# ✅ Create DB and Table if not exists
def init_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rfid TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# 🔁 Initialize DB on app start
init_db()

# 🏠 Home Page
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Attendance Submission Route
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    uid = request.form.get('uid')
    name = request.form.get('name')  # Name field
    rfid = request.form.get('rfid')  # RFID field
    status = request.form.get('status')  # Status field

    if uid and name and rfid and status:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO attendance (name, rfid, status, timestamp, date, uid) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, rfid, status, timestamp, timestamp, uid))  # Insert all required fields
        conn.commit()
        conn.close()
        flash(f"✅ Attendance marked for UID: {uid}", 'success')
        return redirect(url_for('index'))  # Redirect back to home page
    else:
        flash("⚠️ All fields (name, rfid, status, uid) are required!", 'error')
        return redirect(url_for('index'))

# 📊 Dashboard Route
@app.route('/dashboard.html', methods=['GET', 'POST'])
def dashboard():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance ORDER BY timestamp DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', records=records)

# 🚀 Student Registration Route (Handle both GET and POST)
@app.route('/registration.html', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form.get('name')
        roll = request.form.get('roll')
        uid = request.form.get('uid')

        if name and roll and uid:
            conn = sqlite3.connect('student.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name, roll, uid) VALUES (?, ?, ?)", (name, roll, uid))
            conn.commit()
            conn.close()
            flash("✅ Student registered successfully!", 'success')  # Success message
            return redirect(url_for('index'))  # Redirect to home page after registration
        else:
            flash("⚠️ All fields are required!", 'error')  # Error message if fields are missing
            return redirect(url_for('register_student'))  # Redirect back to registration page

    # If GET request, render the registration form
    return render_template('registration.html')

# 🚀 Run the App
if __name__ == '__main__':
    app.run(debug=True)
