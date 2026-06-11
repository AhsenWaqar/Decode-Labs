from .database import get_db_connection

def create_student(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO students(
                full_name,
                email,
                phone,
                gender,
                course,
                semester,
                cgpa
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data['full_name'],
                data['email'],
                data['phone'],
                data['gender'],
                data['course'],
                data['semester'],
                data['cgpa']
            )
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_student_by_id(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return dict(student) if student else None

def get_student_by_email(email, exclude_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if exclude_id:
        cursor.execute("SELECT * FROM students WHERE email = ? AND id != ?", (email, exclude_id))
    else:
        cursor.execute("SELECT * FROM students WHERE email = ?", (email,))
    student = cursor.fetchone()
    conn.close()
    return dict(student) if student else None

def get_all_students(search=None, sort=None, page=1, limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM students"
    params = []
    
    if search:
        query += " WHERE full_name LIKE ? OR email LIKE ? OR course LIKE ?"
        keyword = f"%{search}%"
        params.extend([keyword, keyword, keyword])
        
    ALLOWED_SORT_FIELDS = {
        "name": "full_name",
        "semester": "semester",
        "cgpa": "cgpa"
    }
    
    if sort and sort in ALLOWED_SORT_FIELDS:
        # Safe to inject because it's from a strict whitelist
        query += f" ORDER BY {ALLOWED_SORT_FIELDS[sort]} ASC"
    else:
        query += " ORDER BY id DESC"
        
    # Count total for pagination
    count_query = f"SELECT COUNT(*) FROM ({query})"
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
        
    offset = (page - 1) * limit
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows], total

def update_student(student_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE students
            SET full_name=?,
                email=?,
                phone=?,
                gender=?,
                course=?,
                semester=?,
                cgpa=?
            WHERE id=?
            """,
            (
                data['full_name'],
                data['email'],
                data['phone'],
                data['gender'],
                data['course'],
                data['semester'],
                data['cgpa'],
                student_id
            )
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM students WHERE gender = 'Male'")
    male_students = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM students WHERE gender = 'Female'")
    female_students = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(cgpa) FROM students")
    avg_cgpa = cursor.fetchone()[0]
    if avg_cgpa is None:
        avg_cgpa = 0.0
        
    conn.close()
    
    return {
        "total_students": total_students,
        "male_students": male_students,
        "female_students": female_students,
        "average_cgpa": round(avg_cgpa, 2)
    }
