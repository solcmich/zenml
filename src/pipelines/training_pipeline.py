import os
from datetime import datetime, timezone

from zenml import pipeline
from zenml.config import DockerSettings

from config import TrainingPipelineConfig
from steps.data_loader import load_training_data
from steps.trainer import train_models
from steps.validate_and_deploy import validate_and_deploy_models

ENV = os.environ["ENV"]
STACK = os.environ["STACK"]


@pipeline(
    settings={
        "docker": DockerSettings(
            parent_image="zenmldocker/zenml:0.82.0-py3.11",
            # replicate_local_python_environment="pip_freeze",
            environment={"ENV": ENV, "STACK": STACK}
        ),
    },
    enable_cache=False,
    name=f"{STACK}_training_pipeline_{ENV}",
)
def training_pipeline(config: TrainingPipelineConfig) -> None:
    """Training pipeline for weather prediction models.

    Args:
        config: Pipeline configuration

    """
    # Load training data
    training_data = load_training_data(config)

    # Train models
    trained_models = train_models(training_data, config)

    # Validate and deploy models
    validate_and_deploy_models(trained_models, config)


def run(config: dict, env: str):
    """Run the training pipeline with configuration from YAML.

    Args:
        config: Dictionary containing pipeline configuration loaded from YAML
        env: Environment name (dev/prod)

    """
    data_config = config.get("data", {})
    training_config = config.get("training", {})

    # Convert date strings to datetime objects
    data_range_start = datetime.fromisoformat(
        data_config.get("range_start", "2023-11-01"),
    ).replace(tzinfo=timezone.utc)
    data_range_end = datetime.fromisoformat(
        data_config.get("range_end", "2025-03-22"),
    ).replace(tzinfo=timezone.utc)

    # Create pipeline config
    pipeline_config = TrainingPipelineConfig(
        data_range_start=data_range_start,
        data_range_end=data_range_end,
        **training_config,
        **data_config,
    )

    # Run the pipeline
    training_pipeline(pipeline_config)
