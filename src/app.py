# from flask import Flask, current_app
# from flask_cors import CORS
# from controllers.contact_controller import contact_blueprint
# from controllers.problem_controller import problem_blueprint
# from controllers.transcription_controller import transcription_blueprint
# from controllers.git_controller import git_blueprint
# from controllers.problem_instance_controller import problem_instance_blueprint
# from controllers.subtask_instance_controller import subtask_instance_blueprint
# from controllers.discussion_controller import discussion_blueprint
# from controllers.auth_controller import auth_bp
# from config import Config
# from services.mongo_service import mongo_service
# import sys
# from pathlib import Path


# src_path = Path(__file__).parent.parent
# sys.path.append(str(src_path))

# # Initialize Flask app
# app = Flask(__name__)
# app.config.from_object(Config)

# # Cross-origin cookie/session settings
# app.config.update(
#     SESSION_COOKIE_NAME="session",
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE="Lax",     # 👈 change from 'None' to 'Lax'
#     SESSION_COOKIE_SECURE=False        # 👈 okay for local (no HTTPS)
# )


# # Ensure Flask can manage server-side sessions if needed (optional)
# # app.config["SESSION_TYPE"] = "filesystem"
# # Session(app)  # Uncomment if you use server-side session management

# # Set secret key and Mongo URI
# app.secret_key = app.config["SECRET_KEY"]
# app.config["MONGO_URI"] = "mongodb://localhost:27017/pangea"

# # Enable CORS for cross-origin access with cookies
# CORS(app, supports_credentials=True)

# # Register blueprints
# app.register_blueprint(auth_bp)
# app.register_blueprint(contact_blueprint, url_prefix='/api')
# app.register_blueprint(problem_blueprint, url_prefix='/api')
# app.register_blueprint(transcription_blueprint, url_prefix='/api')
# app.register_blueprint(git_blueprint, url_prefix='/api')
# app.register_blueprint(problem_instance_blueprint, url_prefix='/api')
# app.register_blueprint(subtask_instance_blueprint, url_prefix='/api')
# app.register_blueprint(discussion_blueprint, url_prefix='/api')

# # Initialize services (like MongoDB) after context is available
# def initialize_services():
#     with app.app_context():
#         mongo_service.initialize()

# initialize_services()

# # Start app
# if __name__ == '__main__':
#     try:
#         app.run(host='0.0.0.0', port=5000, debug=True)
#     except OSError:
#         print("Port 5000 is in use, trying port 5001...")
#         app.run(host='0.0.0.0', port=5001, debug=True)

import sys
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Add the project root to Python path
src_path = Path(__file__).parent.parent
sys.path.append(str(src_path))

# Load environment variables
load_dotenv()
from controllers.contact_controller import contact_blueprint
from controllers.problem_controller import problem_blueprint
from controllers.transcription_controller import transcription_blueprint
from controllers.git_controller import git_blueprint
from controllers.problem_instance_controller import problem_instance_blueprint
from controllers.subtask_instance_controller import subtask_instance_blueprint
from controllers.discussion_controller import discussion_blueprint
from controllers.feedback_controller import feedback_blueprint
from controllers.auth_controller import auth_bp
from config import Config
from services.mongo_service import mongo_service

# Initialize Flask app
app = Flask(__name__)

# Load config
from src.config import Config
app.config.from_object(Config)

# Cross-origin cookie/session settings
app.config.update(
    SESSION_COOKIE_NAME="session",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",     # 👈 change from 'None' to 'Lax'
    SESSION_COOKIE_SECURE=False        # 👈 okay for local (no HTTPS)
)

# Set secret key and Mongo URI
app.secret_key = app.config["SECRET_KEY"]
app.config["MONGO_URI"] = "mongodb://localhost:27017/pangea"

# Enable CORS for cross-origin access with cookies
CORS(app,
     resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Import all blueprints
from src.controllers.auth_controller import auth_bp
from src.controllers.contact_controller import contact_blueprint
from src.controllers.problem_controller import problem_blueprint
from src.controllers.transcription_controller import transcription_blueprint
from src.controllers.git_controller import git_blueprint
from src.controllers.problem_instance_controller import problem_instance_blueprint
from src.controllers.subtask_instance_controller import subtask_instance_blueprint
from src.controllers.discussion_controller import discussion_blueprint

# Register all blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(contact_blueprint, url_prefix='/api')
app.register_blueprint(problem_blueprint, url_prefix='/api')
app.register_blueprint(transcription_blueprint, url_prefix='/api')
app.register_blueprint(git_blueprint, url_prefix='/api')
app.register_blueprint(problem_instance_blueprint, url_prefix='/api')
app.register_blueprint(subtask_instance_blueprint, url_prefix='/api')
app.register_blueprint(discussion_blueprint, url_prefix='/api')
app.register_blueprint(feedback_blueprint, url_prefix='/api')

# Initialize MongoDB service
from src.services.mongo_service import mongo_service
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_services():
    with app.app_context():
        try:
            logger.info("Initializing MongoDB service...")
            mongo_service.initialize()
            # Ensure collections exist
            try:
                mongo_service.ensure_collections()
                logger.info("MongoDB collections verified successfully")
            except Exception as collection_error:
                logger.error(f"Error ensuring collections: {str(collection_error)}")
            logger.info("MongoDB service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing services: {str(e)}")
            logger.error("Application will continue, but some features may not work correctly")

# Initialize services
initialize_services()

# Function to check if port is in use
def is_port_in_use(port, host='127.0.0.1'):
    import socket
    import os

    # Skip port check if this is a Flask reloader process
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        return False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

# Start app
if __name__ == '__main__':
    # Get port from command line arguments if provided
    import argparse
    parser = argparse.ArgumentParser(description='Run the Pangea Backend API')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on (default: 5000)')
    parser.add_argument('--force', action='store_true', help='Force the application to use the specified port')
    args = parser.parse_args()

    port = args.port

    # Check if specified port is already in use
    if is_port_in_use(port) and not args.force:
        logger.error(f"Port {port} is already in use!")
        logger.error(f"Please ensure port {port} is available before starting the application.")
        logger.error("To find and kill the process using this port, run one of these commands:")
        logger.error(f"  macOS/Linux: sudo lsof -i :{port} | grep LISTEN")
        logger.error("  followed by: kill -9 <PID>")
        logger.error(f"  Windows: netstat -ano | findstr :{port}")
        logger.error("  followed by: taskkill /F /PID <PID>")
        logger.error("")
        logger.error("You can also:")
        logger.error("1. Use a different port: python3 src/app.py --port 5001")
        logger.error("2. Force using this port (not recommended): python3 src/app.py --force")
        sys.exit(1)  # Exit with error code

    try:
        logger.info(f"Starting server on localhost:{port}")
        app.run(host='127.0.0.1', port=port, debug=True)
    except OSError as e:
        logger.error(f"Failed to start server on localhost:{port}: {str(e)}")
        logger.error(f"Please ensure port {port} is available before starting the application.")
        logger.error("To find and kill the process using this port, run one of these commands:")
        logger.error(f"  macOS/Linux: sudo lsof -i :{port} | grep LISTEN")
        logger.error("  followed by: kill -9 <PID>")
        logger.error(f"  Windows: netstat -ano | findstr :{port}")
        logger.error("  followed by: taskkill /F /PID <PID>")
        sys.exit(1)  # Exit with error code