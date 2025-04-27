from datetime import datetime, timezone

from pydantic import BaseModel, Field


class TrainingPipelineConfig(BaseModel):
    """Configuration for the weather prediction pipeline."""

    # Training parameters
    data_range_start: datetime = Field(
        default=datetime(2023, 11, 1, tzinfo=timezone.utc),
    )
    data_range_end: datetime = Field(default=datetime(2025, 3, 1, tzinfo=timezone.utc))
    test_size: float = Field(default=0.3)
    shuffle: bool = Field(default=False)
    nested: bool = Field(default=False)

    # Model hyperparameters
    n_estimators: int = Field(default=3000)
    depth: int = Field(default=5)
    learning_rate: float = Field(default=0.02)
    early_stopping_rounds: int = Field(default=75)
    l2_leaf_reg: float = Field(default=5)
    random_seed: int = Field(default=42)
    station_ids: list | None = Field(default=None)

    # MLflow settings
    mlflow_tracking_uri: str = Field(default="127.0.0.1:5050")
    mlflow_experiment_name: str = Field(default="weather_prediction")



class DataLoadingPipelineConfig(BaseModel):
    data_source_id: str | None = Field(
        default=None,
        description="ID of data source to download. Can use wildcard * to download multiple, e.g., 'gfs*'",
    )
    new_source_history_length_days: int = Field(
        default=10,
        description="Number of days of history to download for new data sources",
    )
    force_full_history_download: bool = Field(
        default=False, description="Force download of full history even if data exists",
    )
    source_update_cooldown_minutes: int = Field(
        default=30,
        description="Cooldown time in minutes before updating a data source again",
    )
    parallel_downloads: int = Field(
        default=1, description="Number of parallel downloads to run",
    )


class MonitoringConfig(BaseModel):
    log_dir: str | None = Field(default="../storage/reports/")
    reference_data_dir: str | None = Field(default=None)
    station_ids: list[str] | None = Field(default=None)
    prediction_prefix: str = Field(default="prediction_")
    actual_prefix: str = Field(default="actual_")
    output_html_path: str = Field(default="../storage/reports")
