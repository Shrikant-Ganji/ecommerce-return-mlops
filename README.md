# 🛍️ Ecommerce Return Prediction — End-to-End MLOps Project

This repository demonstrates a complete **end-to-end MLOps pipeline** using:

* **Prefect 2.0** for orchestration and scheduled deployments
* **MLflow** for experiment tracking and model registry
* **Evidently AI** for monitoring data drift
* **Scikit-learn + Joblib** for modeling
* **GitHub Codespaces + Render** for development and deployment
* **GitHub Actions** for CI/CD automation
* **Terraform** for Infrastructure as Code (planned)

---

## 🎯 Project Context & Objective

### 📦 Context

Product returns are a significant challenge in the e-commerce industry. They not only affect revenue but also disrupt supply chains and impact customer satisfaction. Companies like Amazon and Flipkart gather extensive data related to orders, customers, payments, shipping, and product reviews. Mining these datasets can reveal patterns that help predict whether a product is likely to be returned.

Understanding the likelihood of a product return **before it happens** allows e-commerce platforms to:

* Reduce logistical costs and losses
* Identify potentially problematic listings or sellers
* Improve customer service and satisfaction
* Implement proactive customer communication or incentives

### 🎯 Objective

The objective of this project is to build a machine learning model to **predict whether a product will be returned** based on historical data from an e-commerce platform and then implement a complete **MLOps workflow** around this model. This includes:

* Loading and preprocessing historical customer/order/product data
* Training and tuning a machine learning model (Random Forest)
* Tracking all experiments and model versions using MLflow
* Orchestrating the pipeline using Prefect 2.0 for scheduled runs
* Containerizing and optionally deploying a FastAPI service
* Monitoring data drift using Evidently AI
* Automating pipeline via GitHub Actions CI/CD
* Preparing infrastructure as code using Terraform for portability

This project simulates a production-grade workflow for real-world deployment and lifecycle management of ML solutions.

---

## 🧰 Tech Stack Overview

| Component              | Tool / Platform            |
| ---------------------- | -------------------------- |
| Cloud/Dev Environment  | GitHub Codespaces + Render |
| Experiment Tracking    | MLflow                     |
| Workflow Orchestration | Prefect 2.0                |
| Monitoring             | Evidently AI               |
| CI/CD                  | GitHub Actions             |
| Infrastructure as Code | Terraform (Render or GCP)  |

---

## 📂 Folder Structure & Module Overview

```bash
├── data/                        # Raw, processed, and prediction data
├── deployment/                 # FastAPI app and Render/K8s deployment config
├── monitoring/                 # Drift detection scripts & HTML reports
├── notebooks/                  # EDA, feature engineering, and training notebooks
├── pipelines/                  # Prefect pipeline script
├── prefect/                    # Prefect CLI configs, monitoring runner
├── src/                        # Source code for training and prediction
├── models/                     # Trained ML model (joblib format)
├── mlruns/, mlflow.db          # MLflow tracking artifacts and metadata
├── .github/workflows/ci.yml    # GitHub Actions pipeline for testing
├── requirements.txt            # Python dependencies
├── prefect.yaml                # Prefect deployment CLI config
├── Dockerfile, Makefile        # Docker & command automation
├── run_deployment.py           # Script for triggering Prefect flow
├── test_predict.py             # Test script for model inference
├── terraform/                  # Infrastructure as Code (Render/GCP)
└── README.md                   # Project documentation
```

---

## 📦 Module Details

### 🗃️ `data/`

* `raw/`: Contains original Olist e-commerce dataset CSVs.
* `processed/`: Preprocessed Parquet files: `train`, `test`, `X`, `y` splits.
* `predictions.csv`: Output file from inference pipeline.

### 🧠 `src/`

* `data_prep.py`: Loads raw data, handles missing values, encodes, and splits.
* `train.py`: Trains a Random Forest model, tracks with MLflow.
* `predict.py`: Generates predictions using the trained model.
* `utils.py`: Shared helper functions.

### 📓 `notebooks/`

* `eda.ipynb`: Explore distributions, missing values, correlations.
* `feature_engineering.ipynb`: Encoding, scaling, and transformation logic.
* `model_training.ipynb`: Model experimentation + MLflow logging walkthrough.

### 🧪 `models/`

* `return_model.joblib`: Final serialized version of the trained model.

### 📁 `mlruns/`, `mlflow.db`

* MLflow tracking backend for:

  * Parameters
  * Metrics (Accuracy, F1-score)
  * Artifacts (model.pkl, conda.yaml, envs)

---

## ⚙️ Prefect 2.0 Orchestration

### 🧵 `pipelines/prefect_flow.py`

Defines `@flow` called `full_pipeline()`:

* Loads → preprocesses → trains → evaluates → predicts → monitors drift

### 🧾 `prefect.yaml`

* CLI-generated deployment config
* Allows you to run via:

```bash
prefect deploy -n "Ecommerce Return Pipeline"
```

### 🧪 `prefect/run_monitoring_flow.py`

* Triggers monitoring task separately via CLI or script

### 🧾 `run_deployment.py`

* On-demand triggering of full Prefect pipeline

---

## 🛰️ Deployment Modules

### ⚙️ `deployment/app.py`

* Optional FastAPI app for serving predictions via `/predict`

### 🧾 `deployment/service.yaml`

* Kubernetes/Render-compatible YAML deployment descriptor

---

## 📊 Monitoring with Evidently

### 🧭 `monitoring/evidently_monitor.py`

* Generates drift report by comparing reference vs current dataset
* Runs as Prefect task or cronjob

### 📊 `monitoring/evidently_report.html`

* Output HTML report from Evidently with visual metrics

---

## ✅ Tests

### 🔍 `test_predict.py`

* Verifies that the saved model loads and makes predictions
* Ensures CI/CD test automation

---

## 🐍 Setup & Usage

### 🔧 Environment Setup

```bash
conda create -n mlops311 python=3.11 -y
conda activate mlops311
pip install -r requirements.txt
```

### 🚦 Start Prefect Server & Worker

```bash
prefect server start
prefect worker start -q default
```

### 🚀 Deploy the Pipeline

```bash
prefect deploy pipelines/prefect_flow.py:full_pipeline \
  -n "Ecommerce Return Pipeline" \
  -q "default" \
  -p "default-agent-pool"
```

### 🔁 Trigger Manual Run

```bash
prefect deployment run 'ecommerce-return-mlops/Ecommerce Return Pipeline'
```

---

## 📈 Output & Artifacts

* 🔹 Drift Report: `monitoring/evidently_report.html`
* 🔹 Tracked Experiments: MLflow UI under `mlruns/`
* 🔹 Serialized Model: `models/return_model.joblib`
* 🔹 Scheduled Deployment: `prefect.yaml`

---

## 🧠 Best Practices Implemented

* ✅ GitHub Codespaces-friendly environment
* ✅ MLflow Tracking + Model Registry
* ✅ Prefect Flow Scheduling and Deployment
* ✅ Lightweight Containerized Deployment (optional)
* ✅ Drift Monitoring with Evidently
* ✅ CI/CD Pipeline with GitHub Actions
* ✅ Infrastructure-as-Code setup scaffold with Terraform

---

## 🏁 Future Enhancements

* 🔁 Automated retraining and model versioning
* 🧪 Unit tests for each module
* 📣 Slack/email alerts for drift detection
* ☁️ Remote artifact logging (S3/GCS/Weights & Biases)
* 🐳 Publish Docker container on Render or GCP

---

## 👨‍💻 Author

**Shrikant Ganji**
🚀 MLOps Zoomcamp | 2025 Edition
🔗 [GitHub](https://github.com/Shrikant-Ganji)
