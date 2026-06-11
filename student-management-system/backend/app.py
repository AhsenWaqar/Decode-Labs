from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.database import init_db
from backend.routes.students import students_bp
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

app.register_blueprint(students_bp, url_prefix='/api')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # Serve corresponding HTML files if requested without extension
    if not os.path.splitext(path)[1]:
        html_path = f"{path}.html"
        if os.path.exists(os.path.join(app.static_folder, html_path)):
            return send_from_directory(app.static_folder, html_path)
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Run the application
    app.run(debug=True, port=5000)
