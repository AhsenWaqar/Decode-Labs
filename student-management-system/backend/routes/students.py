from flask import Blueprint, request
from ..services.student_service import (
    add_student_service, get_students_service, update_student_service,
    delete_student_service
)
from ..models import get_student_by_id, get_dashboard_stats
from ..utils.response import success_response, error_response, validation_error_response

students_bp = Blueprint('students', __name__)

@students_bp.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        stats = get_dashboard_stats()
        return success_response("Dashboard stats retrieved successfully.", stats)
    except Exception:
        return error_response()

@students_bp.route('/students', methods=['POST'])
def add_student():
    data = request.json
    if not data:
        return validation_error_response("No data provided.", {"data": "Empty payload"})
        
    success, message, result = add_student_service(data)
    
    if success:
        return success_response(message, result)
    else:
        if message == "Database error":
            return error_response()
        return validation_error_response(message, result)

@students_bp.route('/students', methods=['GET'])
def get_students():
    try:
        search = request.args.get('search', '')
        sort = request.args.get('sort', '')
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            if page < 1: page = 1
            if limit < 1 or limit > 100: limit = 10
        except ValueError:
            page = 1
            limit = 10
            
        data = get_students_service(search, sort, page, limit)
        return success_response("Students retrieved successfully.", data)
    except Exception:
        return error_response()

@students_bp.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    try:
        student = get_student_by_id(id)
        if student:
            return success_response("Student retrieved successfully.", student)
        return error_response("Student not found.", 404)
    except Exception:
        return error_response()

@students_bp.route('/students/<int:id>', methods=['PUT'])
def update_student_route(id):
    data = request.json
    if not data:
        return validation_error_response("No data provided.", {"data": "Empty payload"})
        
    success, message, errors = update_student_service(id, data)
    
    if success:
        return success_response(message)
    else:
        if message == "Database error":
            return error_response()
        if message == "Student not found":
            return error_response(message, 404)
        return validation_error_response(message, errors)

@students_bp.route('/students/<int:id>', methods=['DELETE'])
def delete_student_route(id):
    success, message = delete_student_service(id)
    if success:
        return success_response(message)
    else:
        if message == "Database error":
            return error_response()
        return error_response(message, 404)
