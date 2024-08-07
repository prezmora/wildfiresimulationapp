from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify(message="Welcome to the Wildfire Prediction API")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    response = {
        'prediction': 'This is a sample prediction response'
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
