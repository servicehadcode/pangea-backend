from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.contact_controller import contact_blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(contact_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=5000, debug=True)