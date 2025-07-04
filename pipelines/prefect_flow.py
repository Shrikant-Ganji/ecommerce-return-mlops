from prefect import flow, task
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

RAW_DATA_PATH = os.path.join("data", "raw")
PROCESSED_DATA_PATH = os.path.join("data", "processed")
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "return_model.joblib")

# Ensure directories exist
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# === Tasks ===

@task(log_prints=True)
def load_data():
    try:
        orders = pd.read_csv(
            os.path.join(RAW_DATA_PATH, "olist_orders.csv"),
            parse_dates=["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"],
        )
        order_items = pd.read_csv(os.path.join(RAW_DATA_PATH, "olist_order_items.csv"))
        products = pd.read_csv(os.path.join(RAW_DATA_PATH, "olist_products.csv"))
        payments = pd.read_csv(os.path.join(RAW_DATA_PATH, "olist_order_payments.csv"))
        reviews = pd.read_csv(os.path.join(RAW_DATA_PATH, "olist_order_reviews.csv"))

        df = (
            orders.merge(order_items, on="order_id", how="inner")
            .merge(products, on="product_id", how="left")
            .merge(payments, on="order_id", how="left")
            .merge(reviews, on="order_id", how="left")
        )
        print("✅ Data loaded successfully")
        return df
    except Exception as e:
        raise RuntimeError(f"❌ Error loading data: {e}")

@task(log_prints=True)
def preprocess(df):
    try:
        df = df[df["order_status"] == "delivered"].copy()
        df["delivery_delay"] = (df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]).dt.days
        df["delivery_time"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days
        df["is_returned"] = df["review_score"].apply(lambda x: 1 if x in [1, 2] else 0)

        features = df[["delivery_delay", "delivery_time", "payment_value", "product_category_name", "is_returned"]].dropna().copy()
        features["product_category_name"] = features["product_category_name"].astype("category").cat.codes
        print("✅ Preprocessing complete")
        return features
    except Exception as e:
        raise RuntimeError(f"❌ Error in preprocessing: {e}")

@task(log_prints=True)
def split_save_data(features):
    try:
        train, test = train_test_split(features, test_size=0.2, random_state=42)
        train_path = os.path.join(PROCESSED_DATA_PATH, "train.parquet")
        test_path = os.path.join(PROCESSED_DATA_PATH, "test.parquet")
        train.to_parquet(train_path, index=False)
        test.to_parquet(test_path, index=False)
        print("✅ Data split and saved")
        return train_path, test_path
    except Exception as e:
        raise RuntimeError(f"❌ Error splitting/saving data: {e}")

@task(log_prints=True)
def train_model(train_path):
    try:
        train = pd.read_parquet(train_path)
        X_train = train.drop("is_returned", axis=1)
        y_train = train["is_returned"]
        model = LogisticRegression(max_iter=200)
        model.fit(X_train, y_train)
        joblib.dump(model, MODEL_PATH)
        print("✅ Model trained and saved")
        return MODEL_PATH
    except Exception as e:
        raise RuntimeError(f"❌ Error training model: {e}")

@task(log_prints=True)
def evaluate_model(test_path, model_path):
    try:
        test = pd.read_parquet(test_path)
        X_test = test.drop("is_returned", axis=1)
        y_test = test["is_returned"]
        model = joblib.load(model_path)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds)
        print(f"✅ Evaluation complete — Accuracy: {acc:.4f}, F1 Score: {f1:.4f}")
        return acc, f1
    except Exception as e:
        raise RuntimeError(f"❌ Error evaluating model: {e}")

@task(log_prints=True)
def predict(test_path, model_path):
    try:
        test = pd.read_parquet(test_path)
        X_test = test.drop("is_returned", axis=1)
        model = joblib.load(model_path)
        preds = model.predict(X_test)
        pred_df = pd.DataFrame({"prediction": preds})
        pred_output_path = os.path.join("data", "predictions.csv")
        pred_df.to_csv(pred_output_path, index=False)
        print(f"✅ Predictions saved to {pred_output_path}")
    except Exception as e:
        raise RuntimeError(f"❌ Error in prediction: {e}")

# === Flow ===

@flow(name="ecommerce-return-mlops")
def full_pipeline():
    df = load_data()
    features = preprocess(df)
    train_path, test_path = split_save_data(features)
    model_path = train_model(train_path)
    evaluate_model(test_path, model_path)
    predict(test_path, model_path)

if __name__ == "__main__":
    full_pipeline()
