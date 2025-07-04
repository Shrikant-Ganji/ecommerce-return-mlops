import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn

# Paths
DATA_PATH = "data/processed/"
MODEL_PATH = "models/return_model.joblib"

# Ensure model directory exists
os.makedirs("models", exist_ok=True)

def load_data():
    X = pd.read_parquet(os.path.join(DATA_PATH, "X_train.parquet"))
    y = pd.read_parquet(os.path.join(DATA_PATH, "y_train.parquet")).squeeze()  # Series
    X_test = pd.read_parquet(os.path.join(DATA_PATH, "X_test.parquet"))
    y_test = pd.read_parquet(os.path.join(DATA_PATH, "y_test.parquet")).squeeze()
    return X, y, X_test, y_test

def train_model(X, y):
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf.fit(X, y)
    return clf

def evaluate_model(clf, X_test, y_test):
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    return acc, f1

def log_experiment(clf, acc, f1):
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("ecommerce-product-return")

    with mlflow.start_run():
        mlflow.log_param("model_type", "RandomForest")
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 10)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)

        mlflow.sklearn.log_model(clf, "return_model")

def save_model(clf):
    joblib.dump(clf, MODEL_PATH)

def main():
    print("🚀 Loading data...")
    X, y, X_test, y_test = load_data()

    print("🧠 Training model...")
    clf = train_model(X, y)

    print("📊 Evaluating model...")
    acc, f1 = evaluate_model(clf, X_test, y_test)
    print(f"✅ Accuracy: {acc:.4f}, F1 Score: {f1:.4f}")

    print("📝 Logging to MLflow...")
    log_experiment(clf, acc, f1)

    print("💾 Saving model...")
    save_model(clf)

    print("✅ Training pipeline complete.")

if __name__ == "__main__":
    main()
