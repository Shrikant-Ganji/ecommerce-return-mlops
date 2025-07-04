from fastapi import FastAPI
from pydantic import create_model
import joblib
import pandas as pd
import os

app = FastAPI()

# === Load model ===
model_path = os.path.join(os.path.dirname(__file__), "../models/return_model.joblib")
model = joblib.load(model_path)

# === Load data schema ===
data_path = os.path.join(os.path.dirname(__file__), "../data/processed/X_train.parquet")
X_train = pd.read_parquet(data_path)
input_features = X_train.columns.tolist()

# Define actual features used during training (important!)
model_input_features = ['delivery_delay', 'delivery_time', 'payment_value', 'product_category_name']

# Create Pydantic input model using all features (for validation)
fields = {col: (float, ...) for col in input_features}
DynamicInput = create_model("DynamicInput", **fields)

@app.get("/")
def read_root():
    return {"message": "E-commerce Return Prediction API is live!"}

@app.post("/predict")
def predict(input_data: DynamicInput):
    try:
        # Convert input to DataFrame
        full_data = pd.DataFrame([input_data.dict()])
        # Select only model-required features
        data = full_data[model_input_features]
        # Predict
        prediction = model.predict(data)[0]
        return {"prediction": int(prediction)}
    except Exception as e:
        return {"error": str(e)}