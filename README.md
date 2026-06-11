In the internship of Decode lab of Full Stack Development in Week 1, I created frontend of student management system
using HTML, CSS, JS. In week 2, I developed APIs using Python. In the week 3, I developed database using SQLite and did integration by modifying my backend APIs. 

Student Management System

A secure, modern, and responsive Student Management System built using HTML, CSS, JavaScript, Python (Flask), and SQLite. This project demonstrates full-stack web development, RESTful API design, database management, and secure coding practices.

 Features
 Dashboard
Total Students
Male Students
Female Students
Average CGPA
Quick Statistics Overview
 Student Management
Add New Student
View All Students
Update Student Information
Delete Student Records
View Student Details
 Search & Filter
Search by Name
Search by Email
Search by Course
Real-time Filtering
 Data Handling
Pagination Support
Sorting by Name, Semester, and CGPA
Data Validation
Duplicate Email Prevention
🛡️ Security Features
Parameterized SQL Queries
SQL Injection Protection
Backend Validation
Frontend Validation
XSS Prevention
Secure Error Handling
Database Constraints Enforcement
 Tech Stack
Frontend
HTML5
CSS3
JavaScript (Vanilla JS)
Fetch API
Backend
Python 3
Flask
Database
SQLite
 Project Structure
student-management-system/
│
├── backend/
│   │
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── validators.py
│   │
│   ├── routes/
│   │   └── students.py
│   │
│   ├── services/
│   │   └── student_service.py
│   │
│   ├── utils/
│   │   └── response.py
│   │
│   └── students.db
│
├── frontend/
│   │
│   ├── index.html
│   ├── students.html
│   ├── add-student.html
│   ├── details.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── api.js
│   │   ├── dashboard.js
│   │   ├── students.js
│   │   ├── add-student.js
│   │   └── details.js
│   │
│   └── assets/
│
├── screenshots/
│
├── requirements.txt
│
└── README.md
 Database Schema
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT NOT NULL
        CHECK(length(trim(full_name)) >= 3),

    email TEXT NOT NULL UNIQUE,

    phone TEXT NOT NULL,

    gender TEXT NOT NULL
        CHECK(gender IN ('Male', 'Female', 'Other')),

    course TEXT NOT NULL,

    semester INTEGER NOT NULL
        CHECK(semester BETWEEN 1 AND 12),

    cgpa REAL NOT NULL
        CHECK(cgpa >= 0.0 AND cgpa <= 4.0),

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
 Installation
1️ Clone Repository
git clone https://github.com/yourusername/student-management-system.git
cd student-management-system
2️ Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Linux / Mac
python3 -m venv venv
source venv/bin/activate
3️ Install Dependencies
pip install -r requirements.txt
4️ Run Application
python app.py

Server starts on:

http://localhost:5000
 API Endpoints
Get All Students
GET /api/students
Get Student By ID
GET /api/students/{id}
Create Student
POST /api/students
Request Body
{
  "full_name": "Ali Khan",
  "email": "ali@gmail.com",
  "phone": "03001234567",
  "gender": "Male",
  "course": "BSCS",
  "semester": 5,
  "cgpa": 3.7
}
Update Student
PUT /api/students/{id}
Delete Student
DELETE /api/students/{id}
Dashboard Statistics
GET /api/dashboard
 Security Considerations
SQL Injection Prevention

All database operations use Parameterized Queries.

Example
cursor.execute(
    "SELECT * FROM students WHERE id = ?",
    (student_id,)
)
Not Allowed
query = f"SELECT * FROM students WHERE id = {student_id}"
Input Validation
Frontend Validation
Required Fields
Email Validation
CGPA Range Validation
Semester Validation
Backend Validation
Duplicate Email Check
Data Type Validation
Business Rules Validation
XSS Protection

User-generated content is rendered safely using:

element.textContent = value;

instead of:

element.innerHTML = value;
 Future Enhancements
Authentication & Authorization
JWT Token-Based Authentication
Student Profile Photos
Attendance Management
Course Management
Export to Excel/CSV
Dark Mode
Audit Logs
Docker Deployment
Unit & Integration Testing
