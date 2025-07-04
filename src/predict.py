import pandas as pd
import joblib
import os

MODEL_PATH = "models/return_model.joblib"
X_TEST_PATH = "data/processed/X_test.parquet"
PREDICTIONS_PATH = "data/predictions.csv"

def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found at {path}")
    return joblib.load(path)

def load_test_data(path=X_TEST_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Test data not found at {path}")
    return pd.read_parquet(path)

def predict(model, X):
    return model.predict(X)

def save_predictions(preds, path=PREDICTIONS_PATH):
    pd.DataFrame({"prediction": preds}).to_csv(path, index=False)
    print(f"✅ Predictions saved to {path}")

if __name__ == "__main__":
    print("📦 Loading model and test data...")
    model = load_model()
    X_test = load_test_data()
    
    print("🔮 Making predictions...")
    preds = predict(model, X_test)
    
    save_predictions(preds)
