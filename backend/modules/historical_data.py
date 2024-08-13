from flask import Blueprint, jsonify, request
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging
import os
import pandas as pd
from modules.model_predict import model_predict  # Import the model_predict function

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

# Database connection settings
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Initialize the blueprint
historical_data_bp = Blueprint('historical_data', __name__)

@historical_data_bp.route('/historical-data', methods=['GET'])
def get_historical_data():
    try:
        # Extract the selected date from the query string
        selected_date = request.args.get('date')
        # logging.debug(f"Selected Date: {selected_date}")
        if not selected_date:
            return jsonify({"error": "No date provided"}), 400

        # Convert the selected_date string into a datetime object
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d')

        # Calculate the start date 30 days before the selected date
        start_date = date_obj - timedelta(days=30)

        # Prepare the SQL query to fetch data between the start and end date
        sql_query = f"""
            SELECT *
            FROM historical_07_12
            WHERE (year, month, day) >= ({start_date.year}, {start_date.month}, {start_date.day})
            AND (year, month, day) <= ({date_obj.year}, {date_obj.month}, {date_obj.day})
        """
        # logging.debug(f"SQL Query: {sql_query}")

        # Connect to the database
        connection = psycopg2.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )
        cursor = connection.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()

        if not data:
            logging.info("No data found for the specified date range.")
            return jsonify({"message": "No data found for the specified date range."}), 200

        # Log the fetched data for debugging purposes
        # logging.debug(f"Database Response Data: {data}")

        # Convert the fetched data to a DataFrame
        columns = [desc[0] for desc in cursor.description]  # Get column names from the cursor
        historical_data_df = pd.DataFrame(data, columns=columns)

        # Log the DataFrame for debugging purposes
        # logging.debug(f"Historical Data DataFrame: {historical_data_df}")

        # Pass the DataFrame to the model_predict function
        predictions = model_predict(historical_data_df)

        return predictions  # This will be a JSON response generated in model_predict

    except Exception as e:
        logging.error(f"Error occurred on Hist   Data: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        if connection:
            cursor.close()
            connection.close()