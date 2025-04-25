import sqlite3

# Create a database connection for attendance (if the database doesn't exist, it will be created)
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# Create the 'attendance' table with a 'timestamp' column
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rfid TEXT NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    uid TEXT NOT NULL
);
""")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Attendance database initialized and table created successfully.")

# Create student.db and students table
conn = sqlite3.connect('student.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll TEXT NOT NULL,
    uid TEXT NOT NULL
);
""")

conn.commit()
conn.close()
print("Student database initialized and table created successfully.")
