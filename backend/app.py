# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation

# For creating the Flask API
from flask import Flask, request, jsonify

# Initialize the Flask application
product_store_sales_predictor_api = Flask("SuperKart Product Store Sales Predictor")

# Load the trained machine learning model
model = joblib.load(serialized_model_file_path)

# Define a route for the home page (GET request)
@product_store_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Product Store Sales Prediction API!"

# Define an endpoint for single property prediction (POST request)
@product_store_sales_predictor_api.post('/v1/predict_sales')
def predict_sales():
    """
    This function handles POST requests to the '/v1/predict_sales' endpoint.
    It expects a JSON payload with current sales, product and store details and returns
    the predicted sales as a JSON response.
    """

    # Get the JSON data from the request body
    request_json = request.get_json()

    # Define product family translation mapping
    product_family_translation = {"Food": "FD", "Drinks": "DR", "Non-Consumables": "NC"}

    # Translate the product_family from user-friendly string to encoded form
    translated_product_family = product_family_translation[request_json['product_family']]

    # Extract relevant features from the JSON data
    extracted_request_json = {
        'Product_Weight': request_json['Product_Weight'],
        'Product_Sugar_Content': request_json['Product_Sugar_Content'],
        'Product_Allocated_Area': request_json['Product_Allocated_Area'],
        'Product_Type': request_json['Product_Type'],
        'Product_MRP': request_json['Product_MRP'],
        'Store_Size': request_json['Store_Size'],
        'Store_Location_City_Type': request_json['Store_Location_City_Type'],
        'Store_Type': request_json['Store_Type'],
        'product_family': translated_product_family, # Use the translated value
        'store_age': request_json['store_age']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_df = pd.DataFrame([extracted_request_json])

    # Make prediction
    predicted_sales = model.predict(input_df)[0]

    # Return the actual price
    return jsonify({
        'Predicted Sales (in dollars)': predicted_sales,
        'status':'success'})


# Define an endpoint for batch prediction (POST request)
@product_store_sales_predictor_api.post('/v1/predict_sales_batch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/predict_sales_batch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame
    predicted_sales = model.predict(input_data).tolist()

    # Create a dictionary of predictions with Store Id as key
    store_ids = input_data['Store_Id'].tolist()
    output_dict = dict(zip(store_ids, predicted_sales))

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    product_store_sales_predictor_api.run(debug=True)
