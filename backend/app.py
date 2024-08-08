from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os
import torch
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Access the environment variables
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_ANON_KEY')
supabase_headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json"
}

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
# model_path = Path("model/best-checkpoint.ckpt")
# wildfire_model = WildfireSimulationModel(model_path)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Wildfire Simulation API"}), 200

@app.route('/api/users')
def get_users():
    try:
        # Making a GET request to Supabase API to list users
        response = requests.get(f"{supabase_url}/auth/v1/users", headers=supabase_headers)
        response.raise_for_status()  # Raises an error for bad responses
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/api/simulation', methods=['POST'])
# def get_simulation():
#     try:
#         # Validate and parse input data
#         data = request.json
#         if not data or 'date' not in data:
#             return jsonify({"error": "Invalid input data"}), 400
        
#         # Assuming input data is properly formatted for your model
#         predictions = wildfire_model.predict(data)

#         # Prepare the response with the prediction data
#         response = {
#             "date": str(data['date']),
#             "predictions": predictions.tolist()  # Convert predictions to list if it's a tensor
#         }
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
