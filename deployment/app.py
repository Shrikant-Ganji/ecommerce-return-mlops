# deployment/app.py

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Add a root route to confirm server is working
@app.get("/")
def read_root():
    return {"message": "E-commerce Return Prediction API is live!"}

# Optional: Sample model input for /predict
class PredictionInput(BaseModel):
    feature1: float
    feature2: float
    # Add all features used in your model

@app.post("/predict")
def predict(data: PredictionInput):
    # Dummy logic – replace with actual model logic
    return {"prediction": 0}
