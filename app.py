import pickle
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the model from pickle file
with open('linear_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint for model inference.
    Expects JSON input with 'features' key containing a list of values.
    Returns prediction as JSON.
    """
    try:
        # Get input features from request
        data = request.get_json(force=True)
        features = data.get('features', [])
        
        # Convert to numpy array and reshape for prediction
        features_array = np.array(features).reshape(-1, 1)
        
        # Make prediction
        prediction = model.predict(features_array)
        
        # Return prediction as JSON
        return jsonify({
            'success': True,
            'prediction': prediction.tolist()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'linear_regression'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
