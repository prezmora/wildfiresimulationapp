from flask import request, jsonify, send_from_directory
from app import app
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/dummy', methods=['GET'])
def dummy_data():
    data = {
        "locations": [
            {"lat": 40.7128, "lon": -74.0060, "intensity": "high"},
            {"lat": 34.0522, "lon": -118.2437, "intensity": "medium"},
            {"lat": 37.7749, "lon": -122.4194, "intensity": "low"}
        ]
    }
    return jsonify(data)
