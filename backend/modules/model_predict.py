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
import __main__

# Load environment variables
load_dotenv()

# Define the blueprint for model predictions
model_predict_bp = Blueprint('model_predict_bp', __name__)

# Load environment-specific paths
TRAIN_DATASET_PATH = os.getenv("TRAIN_DATASET_PATH", "model/train_dataset.pkl")

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


def model_predict(historical_data_df):
    # Ensure historical_data_df is a DataFrame and matches the expected format
    if not isinstance(historical_data_df, pd.DataFrame):
        raise ValueError("historical_data must be a pandas DataFrame")

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

    best_model_path =  os.getenv("BEST_MODEL_PATH", "model/best-checkpoint.ckpt")

    state_dict = torch.load(best_model_path, map_location=torch.device('cpu'))
    best_tft.load_state_dict(state_dict['state_dict'], strict=False)
    best_tft.eval()

    test_filled = pd.DataFrame(historical_data_df)
    validation_dataset = TimeSeriesDataSet.from_dataset(
        train_dataset,
        test_filled,
        predict=True,
        stop_randomization=True,
    )

    batch_size = 64
    val_dataloader = validation_dataset.to_dataloader(train=False, batch_size=batch_size * 10, num_workers=4)

    if next(best_tft.parameters()).is_cuda:
        best_tft = best_tft.cpu()

    test_prediction_results = best_tft.predict(
        val_dataloader,
        mode="raw",
        return_index=True, # return the prediction index in the same order as the output
        return_x=True, # return network inputs in the same order as prediction output
        )

    median_predictions, _ = test_prediction_results.output.prediction.median(dim=1)
    median_predictions = median_predictions.cpu().numpy()[:,1]

    predictions_df = pd.DataFrame(median_predictions, columns=["prediction"])
    predict_merged = pd.concat([test_prediction_results.index, predictions_df], axis=1)
    
    distinct_localities = test_filled[['locality', 'lon', 'lat']].drop_duplicates()
    
    # predict_merged = pd.merge(predictions_df, test_filled[['locality', 'lon', 'lat']], on='locality')
    print("merging",predict_merged)
    print("test_filled",test_filled)
    
    final_merged = pd.merge(predict_merged, distinct_localities, on='locality', how='left')

    # Print or inspect the final merged DataFrame
    print(final_merged)
    
    # Now merge with the original test_filled to include lon and lat based on locality
    # location_df = test_filled[['locality', 'lon', 'lat']].drop_duplicates()  # Ensure no duplicate locality entries
    # final_merged_df = pd.merge(predict_merged, location_df, on='locality', how='left')

    # print("Final Merged DataFrame", final_merged_df)
    
    # Return predictions as JSON
    return jsonify({
        "predictions": predict_merged.to_dict(orient="records"),
        "message": "Predictions generated successfully"
    }), 200

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
        return predictions_df

    except Exception as e:
        return jsonify({"error": str(e)}), 500
