# Flood Prediction System

This project implements a machine learning-based flood prediction system that can predict the likelihood of flooding based on various environmental and geographical factors. It's designed for a hackathon focusing on AI for natural disaster prediction and response.

## Project Components

1. **Dataset Generator**: Creates a synthetic dataset for training the flood prediction model.
2. **ML Model**: Trains, evaluates, and fine-tunes machine learning models to predict flood occurrence.
3. **Web Application**: A Streamlit app for making predictions using the trained model.

## Getting Started

### Prerequisites

Install the required packages:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn xgboost joblib streamlit
```

### Step 1: Generate Dataset(no need to generate as .csv file is already present)

Run the dataset generator script to create the initial training data:

```bash
python generate_dataset.py
```

This will create a file named `flood_prediction_dataset.csv` with synthetic flood data.

### Step 2: Train the Model(it is .ipynb file, run code in second block)

Train the machine learning model using the dataset:
(don't execute this command)
```bash
python train_model.py
```

This script will:
- Perform exploratory data analysis on the dataset
- Train multiple models (Random Forest, Gradient Boosting, XGBoost, Logistic Regression)
- Evaluate model performance
- Fine-tune the best model
- Save the best model as `flood_prediction_model.pkl`

### Step 3: Run the Web Application

Launch the Streamlit web application:

```bash
streamlit run app.py
```

This will start a local web server where you can interact with the flood prediction system.

## Future Improvements

Potential improvements to the system:
1. Incorporate real-time weather data from APIs
2. Add geospatial visualization for risk mapping
3. Implement time-series forecasting for future flooding
4. Add SMS/email alerts for high-risk predictions
5. Develop a mobile application for field use

## Project Structure

```
flood_prediction/
├── generate_dataset.py         # Script to create synthetic dataset
├── train_model.py              # Model training and evaluation
├── app.py                      # Streamlit web application
├── flood_prediction_model.pkl  # Saved trained model
├── flood_prediction_dataset.csv # Generated dataset
└── README.md                   # Project documentation
```
