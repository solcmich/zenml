import logging
import time
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import *
from zenml import step
from zenml.config import DockerSettings
from pipelines.config import MonitoringConfig

logger = logging.getLogger(__name__)

ENV = os.environ["ENV"]
STACK = os.environ["STACK"]

def generate_sample_data(n_samples: int = 1000) -> pd.DataFrame:
    """Generate sample weather data with some drift patterns."""
    np.random.seed(42)
    
    # Generate timestamps
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start=start_date, end=end_date, periods=n_samples)
    
    # Generate features with some drift
    data = {
        'timestamp': dates,
        'temperature': np.random.normal(20, 5, n_samples),  # Reference: mean=20
        'humidity': np.random.normal(65, 10, n_samples),    # Reference: mean=65
        'pressure': np.random.normal(1013, 5, n_samples),   # Reference: mean=1013
        'wind_speed': np.random.normal(5, 2, n_samples),    # Reference: mean=5
        'precipitation': np.random.exponential(0.5, n_samples)  # Reference: mean=0.5
    }
    
    return pd.DataFrame(data)

def generate_current_data(n_samples: int = 1000) -> pd.DataFrame:
    """Generate current weather data with some drift patterns."""
    np.random.seed(43)  # Different seed for current data
    
    # Generate timestamps (last 7 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    dates = pd.date_range(start=start_date, end=end_date, periods=n_samples)
    
    # Generate features with intentional drift
    data = {
        'timestamp': dates,
        'temperature': np.random.normal(22, 5, n_samples),  # Drift: mean=22 (+2)
        'humidity': np.random.normal(70, 10, n_samples),    # Drift: mean=70 (+5)
        'pressure': np.random.normal(1013, 6, n_samples),   # Drift: std=6 (+1)
        'wind_speed': np.random.normal(5, 2, n_samples),    # No drift
        'precipitation': np.random.exponential(0.8, n_samples)  # Drift: mean=0.8 (+0.3)
    }
    
    return pd.DataFrame(data)

@step(
    settings={
        "docker": DockerSettings(
            parent_image="zenmldocker/zenml:py3.11",
            replicate_local_python_environment="pip_freeze",
        ),
    },
    experiment_tracker=f"{STACK}_tracker_{ENV}",
)
def generate_evidently_report(
    config: MonitoringConfig,
) -> None:
    """Generate evidently monitoring report from sample data.
    
    Args:
        config: Monitoring configuration
    """
    logger.info("Mock: Running the evidently monitoring.")
    time.sleep(1)  # Simulate some work
    
    # Generate sample data
    reference_data = generate_sample_data()
    current_data = generate_current_data()
    
    # Save sample data
    os.makedirs(config.reference_data_dir, exist_ok=True)
    reference_data.to_csv(os.path.join(config.reference_data_dir, "reference_data.csv"), index=False)
    current_data.to_csv(os.path.join(config.reference_data_dir, "current_data.csv"), index=False)
    
    logger.info("Mock: Generated sample data with drift patterns")
    
    # Create evidently report
    report = Report(metrics=[
        DataDriftPreset(),
        ColumnDriftMetric(column_name="temperature"),
        ColumnDriftMetric(column_name="humidity"),
        ColumnDriftMetric(column_name="pressure"),
        ColumnDriftMetric(column_name="wind_speed"),
        ColumnDriftMetric(column_name="precipitation"),
        DatasetDriftMetric(),
        DatasetMissingValuesMetric(),
        ColumnSummaryMetric(column_name="temperature"),
        ColumnSummaryMetric(column_name="humidity"),
        ColumnSummaryMetric(column_name="pressure"),
        ColumnSummaryMetric(column_name="wind_speed"),
        ColumnSummaryMetric(column_name="precipitation"),
    ])
    
    # Run the report
    report.run(
        reference_data=reference_data,
        current_data=current_data
    )
    
    # Save the report
    os.makedirs(config.log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(config.log_dir, f"monitoring_report_{timestamp}.html")
    report.save_html(report_path)
    
    logger.info(f"Mock: Generated evidently report at {report_path}")
    logger.info("Mock: Monitoring report generation completed") 