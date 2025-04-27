from flask import Flask, current_app
from flask_cors import CORS
from controllers.contact_controller import contact_blueprint
from controllers.problem_controller import problem_blueprint
from controllers.transcription_controller import transcription_blueprint
from controllers.git_controller import git_blueprint
from controllers.problem_instance_controller import problem_instance_blueprint
from controllers.subtask_instance_controller import subtask_instance_blueprint
from controllers.auth_controller import auth_bp
from config import Config
from services.mongo_service import mongo_service
# from flask_session import Session

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Cross-origin cookie/session settings
app.config.update(
    SESSION_COOKIE_NAME="session",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",     # 👈 change from 'None' to 'Lax'
    SESSION_COOKIE_SECURE=False        # 👈 okay for local (no HTTPS)
)


# Ensure Flask can manage server-side sessions if needed (optional)
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)  # Uncomment if you use server-side session management

# Set secret key and Mongo URI
app.secret_key = app.config["SECRET_KEY"]
app.config["MONGO_URI"] = "mongodb://localhost:27017/pangea"

# Enable CORS for cross-origin access with cookies
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(contact_blueprint, url_prefix='/api')
app.register_blueprint(problem_blueprint, url_prefix='/api')
app.register_blueprint(transcription_blueprint, url_prefix='/api')
app.register_blueprint(git_blueprint, url_prefix='/api')
app.register_blueprint(problem_instance_blueprint, url_prefix='/api')
app.register_blueprint(subtask_instance_blueprint, url_prefix='/api')

# Initialize services (like MongoDB) after context is available
def initialize_services():
    with app.app_context():
        mongo_service.initialize()

initialize_services()

# Start app
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except OSError:
        print("Port 5000 is in use, trying port 5001...")
        app.run(host='0.0.0.0', port=5001, debug=True)