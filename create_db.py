import sqlite3

# Create the attendance table in the 'attendance.db' database
def create_attendance_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_urn TEXT NOT NULL,
        status TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (student_urn) REFERENCES students(roll)
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Attendance database initialized successfully.")

# Create the students table in the 'student.db' database
def create_student_db():
    conn = sqlite3.connect('student.db')  # Connect to 'student.db' instead of 'attendance.db'
    cursor = conn.cursor()

    # Check if the students table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students';")
    table_exists = cursor.fetchone()

    if table_exists:
        # If the students table exists, we need to recreate it
        cursor.execute("PRAGMA foreign_keys=off;")  # Disable foreign key constraint checks temporarily

        # Create a new table with the 'uid' column
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT UNIQUE NOT NULL,
            uid TEXT UNIQUE
        );
        """)

        # Copy data from the old students table to the new one
        cursor.execute("""
        INSERT INTO students_new (id, name, roll)
        SELECT id, name, roll FROM students;
        """)

        # Drop the old students table
        cursor.execute("DROP TABLE students;")

        # Rename the new table to the original name
        cursor.execute("ALTER TABLE students_new RENAME TO students;")
        
        cursor.execute("PRAGMA foreign_keys=on;")  # Enable foreign key constraint checks

        print("✅ UID column added to the students table with UNIQUE constraint.")
    else:
        # Create the students table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT UNIQUE NOT NULL,
            uid TEXT UNIQUE
        );
        """)
        print("✅ Students table created with UID column.")

    conn.commit()
    conn.close()

# Create or update both databases
def initialize_databases():
    create_attendance_db()
    create_student_db()

if __name__ == "__main__":
    initialize_databases()
