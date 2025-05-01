import logging
import time
from zenml import step
from zenml.config import DockerSettings
from config import DataLoadingPipelineConfig

logger = logging.getLogger(__name__)


@step(
    settings={
        "docker": DockerSettings(
            parent_image="zenmldocker/zenml:py3.11",
            replicate_local_python_environment="pip_freeze",
        ),
    },
)
def load_data_sources(
    config: DataLoadingPipelineConfig,
) -> None:
    """Mock version: Simulate loading data from configured data sources.

    Args:
        config: Pipeline configuration
    """
    data_source_id = config.data_source_id if config.data_source_id else "*"
    logger.info(f"Mock: Starting data loading with pattern: {data_source_id}")

    # Simulate loading process
    logger.info("Mock: Simulating data loading...")
    time.sleep(2)  # Simulate some work

    # Create mock data files
    mock_data = {
        "timestamp": "2024-01-01 00:00:00",
        "temperature": 20.5,
        "humidity": 65.0,
        "pressure": 1013.25,
        "wind_speed": 5.0,
    }

    logger.info(f"Mock: Generated sample data: {mock_data}")
    logger.info("Mock: Data loading completed successfully")
