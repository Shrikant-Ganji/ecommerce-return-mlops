# tests/test_predict.py

import os
import sys
import pytest

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import predict  # Now this will work

def test_model_file_exists():
    assert os.path.exists(predict.MODEL_PATH), f"Model file not found at {predict.MODEL_PATH}"

def test_test_data_exists():
    assert os.path.exists(predict.X_TEST_PATH), f"Test data file not found at {predict.X_TEST_PATH}"

def test_load_model():
    model = predict.load_model()
    assert model is not None, "Failed to load model"

def test_load_test_data():
    data = predict.load_test_data()
    assert not data.empty, "Test data is empty"

def test_test_data_columns_match_model():
    model = predict.load_model()
    data = predict.load_test_data()
    model_features = set(model.feature_names_in_)
    data_features = set(data.columns)
    missing_features = model_features - data_features
    assert not missing_features, f"Test data is missing model features: {missing_features}"

def test_predictions_shape():
    model = predict.load_model()
    data = predict.load_test_data()
    # Filter test data to only columns the model expects
    data = data[model.feature_names_in_]
    preds = predict.predict(model, data)
    assert len(preds) == len(data), "Prediction count does not match input data"
