from flask import Flask, jsonify, request, send_from_directory
import requests
from dotenv import load_dotenv
import os
import torch
from pathlib import Path
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='frontend/build')

# Access the environment variables
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_ANON_KEY')
supabase_headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json"
}

# Load locality filter data
with open('data/locality_filter_data.json') as f:
    locality_filter_data = json.load(f)

# Load the Wildfire Simulation Model
class WildfireSimulationModel:
    def __init__(self, model_path):
        # Load the model, assuming it is a PyTorch model
        self.model = torch.load(model_path, map_location=torch.device('cpu'))

    def predict(self, input_data):
        # Convert input data to a tensor, assuming input_data is a dictionary or list of inputs
        input_tensor = torch.tensor(input_data)
        self.model.eval()  # Set the model to evaluation mode
        with torch.no_grad():
            prediction = self.model(input_tensor)
        return prediction

# Load your model (make sure the path is correct)
model_path = Path('model/best-checkpoint.ckpt')
wildfire_model = WildfireSimulationModel(model_path)

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/users')
def get_users():
    try:
        # Making a GET request to Supabase API to list users
        response = requests.get(f"{supabase_url}/auth/v1/users", headers=supabase_headers)
        response.raise_for_status()  # Raises an error for bad responses
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/locality_filters')
def get_locality_filters():
    try:
        # Return the locality filter data
        return jsonify(locality_filter_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/simulation', methods=['POST'])
def get_simulation():
    try:
        # Validate and parse input data
        data = request.json
        if not data or 'date' not in data:
            return jsonify({"error": "Invalid input data"}), 400

        # Prepare the input data for the next 7 days
        predictions = []
        for day in range(7):
            daily_data = data.copy()
            daily_data['date'] += day  # Adjust date for each day
            prediction = wildfire_model.predict(daily_data)
            predictions.append(prediction.item())  # Convert tensor to Python number

        # Prepare the response with the prediction data
        response = {
            "start_date": str(data['date']),
            "predictions": predictions  # List of predictions for the next 7 days
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
