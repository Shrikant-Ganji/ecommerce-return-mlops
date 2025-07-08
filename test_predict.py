import json

import requests

# API URL
url = "https://ecommerce-return-mlops.onrender.com/predict"

# Full input as per API schema
input_data = {
    "delivery_delay": 1.5,
    "delivery_time": 3.2,
    "payment_value": 150.0,
    "product_category_name": 5.0,
    "order_hour": 12.0,
    "late_delivery_flag": 0.0,
}

# Set headers
headers = {"Content-Type": "application/json"}

# Send POST request
response = requests.post(url, data=json.dumps(input_data), headers=headers)

# Print the response
if response.ok:
    print("Prediction response:")
    print(response.json())
else:
    print(f"Failed with status code: {response.status_code}")
    print(response.text)
