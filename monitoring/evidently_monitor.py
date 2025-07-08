# monitoring/evidently_monitor.py

import pandas as pd
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import ColumnDriftMetric
from evidently.report import Report

# Load data
ref_data = pd.read_parquet("data/processed/X_train.parquet")
cur_data = pd.read_parquet("data/processed/X_test.parquet")

# Create report
report = Report(
    metrics=[
        DataDriftPreset(),
        ColumnDriftMetric(column_name="delivery_delay"),
    ]
)

report.run(reference_data=ref_data, current_data=cur_data)
report.save_html("monitoring/evidently_report.html")
print("✅ Evidently report generated at monitoring/evidently_report.html")
