from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.contact_controller import contact_blueprint
from controllers.problem_controller import problem_blueprint
from controllers.transcription_controller import transcription_blueprint
from controllers.git_controller import git_blueprint
from controllers.problem_instance_controller import problem_instance_blueprint
from controllers.subtask_instance_controller import subtask_instance_blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(contact_blueprint, url_prefix='/api')
app.register_blueprint(problem_blueprint, url_prefix='/api')
app.register_blueprint(transcription_blueprint, url_prefix='/api')
app.register_blueprint(git_blueprint, url_prefix='/api')
app.register_blueprint(problem_instance_blueprint, url_prefix='/api')
app.register_blueprint(subtask_instance_blueprint, url_prefix='/api')

if __name__ == '__main__':
    # Try a different port if 5000 is in use
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except OSError:
        print("Port 5000 is in use, trying port 5001...")
        app.run(host='0.0.0.0', port=5001, debug=True)