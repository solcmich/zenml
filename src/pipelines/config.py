from datetime import datetime, timezone

from pydantic import BaseModel, Field


class TrainingPipelineConfig(BaseModel):
    # Model hyperparameters
    dummy: int = Field(default=3000)



class DataLoadingPipelineConfig(BaseModel):
    dummy: int = Field(default=3000)


class MonitoringConfig(BaseModel):
    log_dir: str | None = Field(default="../storage/reports/")
    reference_data_dir: str | None = Field(default=None)
