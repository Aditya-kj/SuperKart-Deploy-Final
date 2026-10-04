import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SuperKart Sales Predictor", layout="centered")

st.title("🛒 SuperKart Sales Prediction App")
st.write("Enter product and store details below or upload a batch file to predict total sales.")

# Define the API endpoint (assuming backend runs on port 7860)
BACKEND_URL = "http://localhost:7860/v1/predict"
BATCH_URL = "http://localhost:7860/v1/predictbatch"

tab1, tab2 = st.tabs(["Single Prediction", "Batch Prediction"])

with tab1:
    st.header("Single Item Prediction")
    
    col1, col2 = st.columns(2)
    with col1:
        product_weight = st.number_input("Product Weight", value=12.5)
        product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        product_allocated_area = st.number_input("Product Allocated Area (Ratio)", value=0.05)
        product_mrp = st.number_input("Product MRP", value=150.0)
        store_size = st.selectbox("Store Size", ["Medium", "High", "Small"])
        
    with col2:
        store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Grocery Store", "Departmental Store"])
        product_id_char = st.selectbox("Product ID Prefix", ["FD", "DR", "NC"])
        store_age_years = st.number_input("Store Age (Years)", value=15, min_value=0, max_value=100)
        product_type_category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

    if st.button("Predict Sales"):
        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar_content,
            "Product_Allocated_Area": product_allocated_area,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": store_location_city_type,
            "Store_Type": store_type,
            "Product_Id_char": product_id_char,
            "Store_Age_Years": store_age_years,
            "Product_Type_Category": product_type_category
        }
        
        try:
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"🎉 Predicted Total Store Sales: ${result['Predicted_Sales']:,.2f}")
            else:
                st.error(f"Server Error: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to backend API: {e}")

with tab2:
    st.header("Batch Prediction via CSV Upload")
    st.write("Upload a CSV file containing the exact 10 required features.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="user_data.csv")
    
    if uploaded_file is not None:
        if st.button("Run Batch Prediction"):
            try:
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(BATCH_URL, files=files)
                if response.status_code == 200:
                    preds = response.json()
                    res_df = pd.DataFrame(list(preds.items()), columns=["Row Index", "Predicted Sales"])
                    st.success("✅ Batch Prediction Successful!")
                    st.dataframe(res_df)
                else:
                    st.error(f"Server Error: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend API: {e}")
