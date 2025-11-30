# app.py

import numpy as np
import pickle
from flask import Flask, request, jsonify

# Load the model from the saved file
try:
    with open('linear_regression_model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    print("Error: linear_regression_model.pkl not found. Ensure Train_and_save.ipynb was run to generate the model.")
    exit()

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Accepts JSON data with California Housing features and returns predicted price.
    Supports three formats:
    1. Array format: {"features": [8.3, 41.0, 6.98, 1.02, 2332.0, 4.11, 37.88, -122.23]}
    2. Object format: {"MedInc": 8.3, "HouseAge": 41.0, "AveRooms": 6.98, "AveBedrms": 1.02, "Population": 2332.0, "AveOccup": 4.11, "Latitude": 37.88, "Longitude": -122.23}
    3. Nested data format: {"data": [{"MedInc": 8.3, "HouseAge": 41.0, ...}]}
    """
    try:
        data = request.get_json()
        
        # Handle nested "data" format
        if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
            data = data['data'][0]
        
        # Handle array format
        if 'features' in data and isinstance(data['features'], list):
            features = data['features']
        else:
            # Handle object format
            feature_names = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
            features = [data[name] for name in feature_names]
        
        # Model expects a 2D array: [[feature1, feature2, ..., feature8]]
        input_data = np.array([features])

        # Make the prediction
        prediction = model.predict(input_data)[0]

        # Return the prediction as JSON
        return jsonify({
            'features': features,
            'PredictedPrice': float(prediction)
        })

    except KeyError as e:
        return jsonify({'error': f'Missing required feature: {e}'}), 400
    except Exception as e:
        return jsonify({'error': f'Invalid input format or prediction error: {e}'}), 400

if __name__ == '__main__':
    # Use Gunicorn in the container, but Flask's built-in server for local testing
    app.run(debug=True, host='0.0.0.0', port=5000)