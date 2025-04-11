from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.contact_controller import contact_blueprint
from controllers.problem_controller import problem_blueprint
from controllers.transcription_controller import transcription_blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(contact_blueprint, url_prefix='/api')
app.register_blueprint(problem_blueprint, url_prefix='/api')
app.register_blueprint(transcription_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)