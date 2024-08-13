import os
import pickle
import torch
import pandas as pd
from flask import Blueprint, jsonify, request
from pytorch_forecasting import TimeSeriesDataSet
from pytorch_forecasting.models import TemporalFusionTransformer
from pytorch_forecasting.metrics import QuantileLoss
from dotenv import load_dotenv
import types
import __main__  # Used for workaround 2

# Load environment variables
load_dotenv()

# Define the blueprint for model predictions
model_predict_bp = Blueprint('model_predict_bp', __name__)

# Load environment-specific paths
TRAIN_DATASET_PATH = os.getenv("TRAIN_DATASET_PATH", "/workspace/wildfiresimulationapp/backend/model/train_dataset.pkl")
BEST_MODEL_PATH = os.getenv("BEST_MODEL_PATH", "/workspace/wildfiresimulationapp/backend/model/best-checkpoint.ckpt")

# Load the training dataset (metadata) required to create TimeSeriesDataSet objects
with open(TRAIN_DATASET_PATH, "rb") as f:
    train_dataset = pickle.load(f)

# Define custom weighted quantile loss
class WeightedQuantileLoss(QuantileLoss):
    def __init__(self, zero_weight=1.0, non_zero_weight=10.0, **kwargs):
        super().__init__(**kwargs)
        self.zero_weight = zero_weight
        self.non_zero_weight = non_zero_weight

    def loss(self, y_pred, y_actual):
        base_loss = super().loss(y_pred, y_actual)
        weights = torch.where(y_actual == 0, self.zero_weight, self.non_zero_weight)
        
        # Expand weights to match the shape of base_loss
        weights = weights.unsqueeze(-1).expand_as(base_loss)
        
        return (base_loss * weights).mean()

# Inject WeightedQuantileLoss into __main__ module (Workaround 2)
setattr(__main__, 'WeightedQuantileLoss', WeightedQuantileLoss)

# Define the model
# Use the weighted loss in the model definition
best_tft = TemporalFusionTransformer.from_dataset(
    train_dataset,
    learning_rate=1e-3,
    hidden_size=64,
    attention_head_size=4,
    dropout=0.1,
    hidden_continuous_size=32,
   # output_size=7,  # number of quantiles
    loss=WeightedQuantileLoss(zero_weight=1.0, non_zero_weight=10.0),  # Adjust weights as needed
    log_interval=10,
    reduce_on_plateau_patience=10
)

# Load the trained TemporalFusionTransformer model
def load_model(best_model_path):
    # Load the model with the custom loss function now available in the global namespace
    state_dict = torch.load(best_model_path, map_location=torch.device('cpu'))
    best_tft.load_state_dict(state_dict['state_dict'], strict=False)
    best_tft.eval()  # Set the model to evaluation mode
    return best_tft

def model_predict(historical_data_df):
    # Ensure historical_data_df is a DataFrame and matches the expected format
    # print("Xthis is it", historical_data_df)
    if not isinstance(historical_data_df, pd.DataFrame):
        raise ValueError("historical_data must be a pandas    DataFrame")

    
    # print("traindataset", train_dataset)
    print("before validation dataset")
    # Prepare the validation dataset based on historical data
    validation_dataset = TimeSeriesDataSet.from_dataset(
        train_dataset,
        historical_data_df,
        predict=True,
        stop_randomization=True,
    )
    
    print("validation_dataset", validation_dataset)
    # Prepare dataloader
    batch_size = 64
    val_dataloader = validation_dataset.to_dataloader(train=False, batch_size=batch_size * 10, num_workers=4)
  
    # Load the best model using the new load_model function
    # best_tft = load_model(BEST_MODEL_PATH)
    
    # Move the model to CPU if necessary (this should already be done in load_model)
    if next(best_tft.parameters()).is_cuda:
        best_tft = best_tft.cpu()

    # Generate predictions
    predictions = best_tft.predict(val_dataloader)
    
    # print("this is it", predictions)

    # Convert predictions to DataFrame for easier manipulation
    predictions_df = pd.DataFrame(predictions, columns=['prediction'])

   # Extract the corresponding lat and lon from historical_data_df
    # You can use the locality or other identifiers to ensure the correct matching
    # combined_df = pd.concat([historical_data_df[['time_idx', 'locality', 'lat', 'lon', 'cfb']], predictions_df], axis=1)


    # Return predictions as a JSON response
    return predictions_df

# Flask route for handling prediction requests
@model_predict_bp.route('/predict', methods=['POST'])
def predict_route():
    try:
        # Get historical data from the request body
        historical_data = request.json.get('historical_data')
        if not historical_data:
            return jsonify({"error": "No historical data provided"}), 400
        
        # Convert to DataFrame
        historical_data_df = pd.DataFrame(historical_data)

        # Run predictions
        predictions_df = model_predict(historical_data_df)

        # Return predictions to the frontend
        return jsonify({
            "predictions": predictions_df.to_dict(orient='records'),
            "message": "Data retrieved and predictions generated successfully"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
