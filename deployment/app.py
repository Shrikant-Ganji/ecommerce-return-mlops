# deployment/app.py

from fastapi import FastAPI
from pydantic import BaseModel, create_model
import joblib
import pandas as pd
import os

app = FastAPI()

# === Load model ===
model_path = os.path.join(os.path.dirname(__file__), "../models/return_model.joblib")
model = joblib.load(model_path)

# === Dynamically generate input model based on train.parquet ===
data_path = os.path.join(os.path.dirname(__file__), "../data/processed/X_train.parquet")
X_train = pd.read_parquet(data_path)
input_features = X_train.columns.tolist()

# Dynamically create Pydantic input model
fields = {col: (float, ...) for col in input_features}
DynamicInput = create_model("DynamicInput", **fields)

@app.get("/")
def read_root():
    return {"message": "E-commerce Return Prediction API is live!"}

@app.post("/predict")
def predict(input_data: DynamicInput):
    data = pd.DataFrame([input_data.dict()])
    prediction = model.predict(data)[0]
    return {"prediction": int(prediction)}
