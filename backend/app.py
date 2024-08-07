from flask_cors import CORS
from app import app

# Enable CORS for all routes
CORS(app)

@app.route('/')
def index():
    return "Welcome to the Wildfire Prediction App API"

