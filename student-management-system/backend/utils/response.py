from flask import jsonify

def success_response(message="Operation completed successfully.", data=None):
    response = {
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    }
    return jsonify(response), 200

def error_response(message="An unexpected error occurred.", status_code=500):
    response = {
        "success": False,
        "message": message
    }
    return jsonify(response), status_code

def validation_error_response(message="Validation failed.", errors=None):
    response = {
        "success": False,
        "message": message,
        "errors": errors if errors is not None else {}
    }
    return jsonify(response), 400
