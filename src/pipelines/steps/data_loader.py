import logging
import time
import pandas as pd
import numpy as np
from zenml import step
from zenml.config import DockerSettings
from config import TrainingPipelineConfig

logger = logging.getLogger(__name__)


@step(
    settings={
        "docker": DockerSettings(
            parent_image="zenmldocker/zenml:py3.11",
            replicate_local_python_environment="pip_freeze",
        ),
    },
)
def load_training_data(config: TrainingPipelineConfig) -> dict:
    """Mock version: Generate synthetic training data.

    Args:
        config: Pipeline configuration
        data_storage_db: Database connection (not used in mock)

    Returns:
        pd.DataFrame: Synthetic training data
    """
    logger.info("Mock: Generating synthetic training data...")
    time.sleep(1)  # Simulate some work

    # Generate synthetic data
    np.random.seed(42)
    n_samples = 1000

    # Generate features
    data = {
        # 'timestamp': dates,
        "temperature": np.random.normal(20, 5, n_samples),
        "humidity": np.random.normal(65, 10, n_samples),
        "pressure": np.random.normal(1013, 5, n_samples),
        "wind_speed": np.random.normal(5, 2, n_samples),
        "station_id": np.random.choice(["station1", "station2", "station3"], n_samples),
    }

    df = pd.DataFrame(data)
    logger.info(f"Mock: Generated {len(df)} samples of training data")
    rv = {"station_mockup": df}
    return rv
