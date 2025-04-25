# RFID Smart Attendance System 

A Flask-based RFID Attendance System that stores and displays student attendance records using an SQLite database.

## 🔧 Features

- 🖥️ Web-based interface using Flask and HTML templates
- 🎫 Student registration with RFID
- ✅ Attendance logging with RFID card scanning
- 📊 Dashboard to view attendance records
- 💾 Data stored locally in `SQLite` database

## 📁 Project Structure

/SmartAttendance ├── app.py # Main Flask app ├── create_db.py # Script to initialize the attendance DB ├── student.db # (Optional) DB for student details ├── attendance.db # Attendance records database ├── templates/ │ ├── index.html │ ├── registration.html │ └── dashboard.html └── static/ └── style.css # (Add your CSS here)

bash
Copy
Edit

## 🧪 Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SmartAttendance.git
   cd SmartAttendance
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Initialize the database:

bash
Copy
Edit
python create_db.py
Run the Flask server:

bash
Copy
Edit
python app.py
Open your browser:

cpp
Copy
Edit
http://127.0.0.1:5000
🚀 Deployment
For hosting this app online, you can use Render.com. Simply connect your GitHub repo, and follow the steps to deploy a Python web service.

🧠 Tech Stack
Python

Flask

SQLite

HTML/CSS

