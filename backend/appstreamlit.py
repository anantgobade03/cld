import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the model
@st.cache_resource
def load_model():
    model = joblib.load("flood_prediction_model.pkl")
    return model

# Function to make predictions
def predict_flood_risk(model, data_point):
    df = pd.DataFrame([data_point])
    proba = model.predict_proba(df)[0, 1]
    prediction = 1 if proba >= 0.5 else 0
    risk_level = "Low" if proba < 0.3 else "Medium" if proba < 0.7 else "High"
    return {"probability": proba, "prediction": prediction, "risk_level": risk_level}

# Main app
def main():
    st.set_page_config(page_title="Flood Risk Prediction System", layout="wide")
    st.title("Flood Risk Prediction System")
    st.write("This application predicts the risk of flooding based on environmental factors.")
    
    if not os.path.exists("flood_prediction_model.pkl"):
        st.error("Model file not found. Please run the training script first.")
        return
    
    model = load_model()
    
    st.sidebar.header("Input Parameters")
    
    # Date inputs
    st.sidebar.subheader("Date")
    year = st.sidebar.number_input("Year", min_value=2000, max_value=2030, value=2023)
    month = st.sidebar.slider("Month", 1, 12, 6)
    day = st.sidebar.slider("Day", 1, 31, 15)
    
    # Weather inputs
    st.sidebar.subheader("Weather Conditions")
    rainfall_24h = st.sidebar.slider("24-Hour Rainfall (mm)", 0.0, 200.0, 50.0, 0.1)
    rainfall_72h = st.sidebar.slider("72-Hour Rainfall (mm)", 0.0, 300.0, 100.0, 0.1)
    temperature = st.sidebar.slider("Temperature (°C)", -10.0, 40.0, 20.0, 0.1)
    
    # Water levels
    st.sidebar.subheader("Water Levels")
    river_level = st.sidebar.slider("River Level (m)", 0.0, 5.0, 1.5, 0.01)
    soil_moisture = st.sidebar.slider("Soil Moisture (%)", 0.0, 100.0, 50.0, 0.1)
    
    # Predefined values
    snowmelt = 0.0  # Fixed
    reservoir_level = 75.0  # Optimal predefined value
    slope_gradient = 10.0  # Optimal predefined value
    vegetation_cover = 60.0  # Optimal predefined value
    urbanization = 40.0  # Optimal predefined value
    previous_floods = st.sidebar.selectbox("Previous Floods in Last Month", [0, 1])
    
    data_point = {
        'rainfall_24h': rainfall_24h,
        'rainfall_72h': rainfall_72h,
        'river_level': river_level,
        'soil_moisture': soil_moisture,
        'slope_gradient': slope_gradient,
        'vegetation_cover': vegetation_cover,
        'urbanization': urbanization,
        'temperature': temperature,
        'snowmelt': snowmelt,
        'reservoir_level': reservoir_level,
        'previous_floods': previous_floods,
        'year': year,
        'month': month,
        'day': day
    }
    
    st.header("Prediction")
    if st.button("Predict Flood Risk"):
        prediction = predict_flood_risk(model, data_point)
        
        # Probability gauge
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xticks([0, 0.3, 0.7, 1])
        ax.set_xticklabels(['0%', '30%', '70%', '100%'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Create gradient background
        cmap = plt.cm.get_cmap('RdYlGn_r')
        for i in range(100):
            ax.axvspan(i/100, (i+1)/100, color=cmap(i/100), alpha=0.3)
        
        # Add indicator arrow
        ax.arrow(prediction['probability'], 0.5, 0, 0.2, width=0.03, head_width=0.05, 
                 head_length=0.1, fc='black', ec='black')
        
        # Add risk labels
        ax.text(0.15, 0.2, "LOW RISK", ha='center', fontsize=12)
        ax.text(0.5, 0.2, "MEDIUM RISK", ha='center', fontsize=12)
        ax.text(0.85, 0.2, "HIGH RISK", ha='center', fontsize=12)
        
        st.pyplot(fig)
        
        # Display prediction results
        st.metric("Flood Probability", f"{prediction['probability']:.1%}")
        st.metric("Prediction", "Flood" if prediction['prediction'] == 1 else "No Flood")
        st.metric("Risk Level", prediction['risk_level'])
    
if __name__ == "__main__":
    main()
