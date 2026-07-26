import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:5000"

# Set the title of the Streamlit app
st.title("SuperKart Product-Store Sales Prediction")

# SINGLE RECORD Prediction section
st.subheader("Single Record Prediction")

# Collect user input for SuperKart features
product_weight = st.number_input("Product Weight", format="%.2f")
product_sugar_content = st.selectbox("Product Sugar Content", ['Low Sugar', 'Regular', 'No Sugar'])
product_allocated_area = st.number_input("Product Allocated Area", format="%.3f")
product_type = st.selectbox("Product Type", ['Fruits and Vegetables', 'Snack Foods', 'Household', 'Frozen Foods', 'Dairy', 'Canned', 'Baking Goods', 'Health and Hygiene', 'Soft Drinks', 'Meat', 'Hard Drinks', 'Breads', 'Breakfast', 'Starchy Foods', 'Others', 'Seafood'])
product_mrp = st.number_input("Product MRP", format="%.2f")

store_size = st.selectbox("Store Size", ['Small', 'Medium', 'High'])
store_location_city_type = st.selectbox("Store Location City Type",["Tier 3","Tier 2","Tier 1"])
store_type = st.selectbox("Store Type",["Departmental Store","Food Mart","Supermarket Type1","Supermarket Type2"])

# Display user-friendly names, and send these to the backend for translation
product_family_options_display = {"FD": "Food", "DR": "Drinks", "NC": "Non-Consumables"}
selected_product_family_display = st.selectbox("Product Family", list(product_family_options_display.keys()))

store_age = st.number_input("Store Age", format="%d")

# Convert user input into a DataFrame (sending user-friendly product_family)
input_data = pd.DataFrame([{
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_Type': product_type,
    'Product_MRP': product_mrp,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'product_family': selected_product_family_display,
    'store_age': store_age
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict_sales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Sales (in dollars)']
        st.success(f"Predicted Sales (in dollars): {prediction}")
    else:
        st.error(f"Unable to connect to the prediction API. Error: {response.status_code} - {response.text}")


# BATCH PREDICTION section
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predict_sales_batch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error(f"Unable to connect to the prediction API. Error: {response.status_code} - {response.text}")
