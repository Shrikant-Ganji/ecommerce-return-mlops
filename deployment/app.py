from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel

app = FastAPI()
model = joblib.load("models/return_model.joblib")

class InputData(BaseModel):
    delivery_delay: int
    delivery_time: int
    payment_value: float
    product_category_name: int

@app.post("/predict")
def predict(data: InputData):
    df = pd.DataFrame([data.dict()])
    pred = model.predict(df)
    return {"prediction": int(pred[0])}
