from ..models import (
    create_student, get_student_by_id, get_student_by_email, 
    get_all_students, update_student, delete_student, get_dashboard_stats
)
from ..validators import validate_student_data

def add_student_service(data):
    errors = validate_student_data(data)
    if errors:
        return False, "Validation failed", errors
        
    # Check duplicate email
    if get_student_by_email(data['email']):
        return False, "Validation failed", {"email": "Email already exists"}
        
    try:
        student_id = create_student(data)
        return True, "Student created successfully", {"id": student_id}
    except Exception as e:
        return False, "Database error", str(e)

def get_students_service(search, sort, page, limit):
    students, total = get_all_students(search, sort, page, limit)
    return {
        "students": students,
        "total": total,
        "page": page,
        "limit": limit
    }

def update_student_service(student_id, data):
    errors = validate_student_data(data)
    if errors:
        return False, "Validation failed", errors
        
    # Check if student exists
    if not get_student_by_id(student_id):
        return False, "Student not found", {}
        
    # Check duplicate email excluding current
    if get_student_by_email(data['email'], exclude_id=student_id):
        return False, "Validation failed", {"email": "Email already exists"}
        
    try:
        success = update_student(student_id, data)
        if success:
            return True, "Student updated successfully", None
        return False, "Student not found", None
    except Exception as e:
        return False, "Database error", str(e)

def delete_student_service(student_id):
    if not get_student_by_id(student_id):
        return False, "Student not found"
        
    try:
        success = delete_student(student_id)
        return success, "Student deleted successfully" if success else "Failed to delete"
    except Exception as e:
        return False, "Database error"
