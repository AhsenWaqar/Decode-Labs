import re

def validate_student_data(data):
    errors = {}
    
    # Full Name
    full_name = str(data.get('full_name', '')).strip()
    if not full_name:
        errors['full_name'] = "Full name is required."
    elif len(full_name) < 3 or len(full_name) > 100:
        errors['full_name'] = "Full name must be between 3 and 100 characters."
        
    # Email
    email = str(data.get('email', '')).strip()
    if not email:
        errors['email'] = "Email is required."
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors['email'] = "Invalid email format."
        
    # Phone
    phone = str(data.get('phone', '')).strip()
    if not phone:
        errors['phone'] = "Phone number is required."
    elif not re.match(r"^\d{10,15}$", phone):
        errors['phone'] = "Phone must be 10-15 digits."
        
    # Gender
    gender = str(data.get('gender', ''))
    if gender not in ['Male', 'Female', 'Other']:
        errors['gender'] = "Gender must be Male, Female, or Other."
        
    # Course
    course = str(data.get('course', '')).strip()
    if not course:
        errors['course'] = "Course is required."
        
    # Semester
    try:
        semester = int(data.get('semester', 0))
        if semester < 1 or semester > 12:
            errors['semester'] = "Semester must be between 1 and 12."
    except ValueError:
        errors['semester'] = "Semester must be a valid integer."
        
    # CGPA
    try:
        cgpa = float(data.get('cgpa', -1.0))
        if cgpa < 0.0 or cgpa > 4.0:
            errors['cgpa'] = "CGPA must be between 0 and 4."
    except ValueError:
        errors['cgpa'] = "CGPA must be a valid number."
        
    return errors
