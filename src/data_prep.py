import pandas as pd
from sklearn.model_selection import train_test_split
import os

RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"

os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

def load_data():
    orders = pd.read_csv(
        RAW_DATA_PATH + "olist_orders.csv",
        parse_dates=["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]
    )
    order_items = pd.read_csv(RAW_DATA_PATH + "olist_order_items.csv")
    products = pd.read_csv(RAW_DATA_PATH + "olist_products.csv")
    payments = pd.read_csv(RAW_DATA_PATH + "olist_order_payments.csv")
    reviews = pd.read_csv(RAW_DATA_PATH + "olist_order_reviews.csv")
    
    df = orders.merge(order_items, on="order_id", how="inner") \
               .merge(products, on="product_id", how="left") \
               .merge(payments, on="order_id", how="left") \
               .merge(reviews, on="order_id", how="left")

    return df

def preprocess(df):
    # Keep only delivered orders
    df = df[df["order_status"] == "delivered"].copy()

    # Calculate delivery delay and time
    df.loc[:, "delivery_delay"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.days

    df.loc[:, "delivery_time"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days

    # Label returns based on review score
    df.loc[:, "is_returned"] = df["review_score"].apply(lambda x: 1 if x in [1, 2] else 0)

    # **Include order_purchase_timestamp for feature engineering**
    # Also include order_id if needed for merges or tracking
    features = df[[
        "order_id",                      # for traceability (optional)
        "order_purchase_timestamp",     # needed for hour extraction
        "delivery_delay",
        "delivery_time",
        "payment_value",
        "product_category_name",
        "is_returned"
    ]].dropna().copy()

    # Encode categorical feature
    features.loc[:, "product_category_name"] = features["product_category_name"].astype("category").cat.codes

    return features

def save(features):
    train, test = train_test_split(features, test_size=0.2, random_state=42)
    train.to_parquet(PROCESSED_DATA_PATH + "train.parquet", index=False)
    test.to_parquet(PROCESSED_DATA_PATH + "test.parquet", index=False)

if __name__ == "__main__":
    df = load_data()
    features = preprocess(df)
    save(features)
    print("✅ Preprocessing done. Saved to data/processed/")
