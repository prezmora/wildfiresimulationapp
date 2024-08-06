import requests
from flask import request, jsonify, send_from_directory
from app import app
from supabase import create_client, Client
import os
import torch
from dotenv import load_dotenv
from app.auth.user_utils import load_users
from flask_cors import CORS

# Add CORS support to your app
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# URL of the dummy model file
MODEL_URL = os.getenv('MODEL_URL')

# Download the dummy model file
response = requests.get(MODEL_URL)
with open('model.pth', 'wb') as f:
    f.write(response.content)

# Dummy model class
class TemporalFusionTransformer(torch.nn.Module):
    def __init__(self):
        super(TemporalFusionTransformer, self).__init__()
        self.linear = torch.nn.Linear(3, 1)  # Example with input size 3 and output size 1

    def forward(self, x):
        return self.linear(x)  # Dummy forward pass

model = TemporalFusionTransformer()
model.load_state_dict(torch.load('model.pth'))
model.eval()

@app.route('/')
def index():
    return "Welcome to the Wildfire Prediction App API"

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    try:
        user = supabase.auth.sign_up(email=email, password=password)
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    try:
        user = supabase.auth.sign_in(email=email, password=password)
        return jsonify({'message': 'Login successful'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 401

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_tensor = torch.tensor(data['inputs'], dtype=torch.float32)
    with torch.no_grad():
        prediction = model(input_tensor).numpy().tolist()
    return jsonify({'prediction': prediction})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

