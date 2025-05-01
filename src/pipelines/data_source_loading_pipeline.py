from zenml import pipeline
from config import DataLoadingPipelineConfig
from steps.data_source_loader import load_data_sources
import os
from zenml.config import DockerSettings

ENV = os.environ["ENV"]
STACK = os.environ["STACK"]


@pipeline(
    enable_cache=False,
    settings={
        "docker": DockerSettings(
            parent_image="zenmldocker/zenml:py3.11",
            # replicate_local_python_environment="pip_freeze",
            environment={"ENV": ENV, "STACK": STACK},
        ),
    },
    name=f"{STACK}_data_source_loading_pipeline_{ENV}",
)
def data_source_loading_pipeline(config: DataLoadingPipelineConfig) -> None:
    """Pipeline for loading data from various sources."""
    # Load data from sources
    load_data_sources(config)


def run(config: dict, env: str):
    """Run the data loading pipeline with configuration from YAML.

    Args:
        config: Dictionary containing pipeline configuration loaded from YAML
        env: Environment name (dev/test/prod)
    """
    # Run the pipeline with configuration from YAML
    config = DataLoadingPipelineConfig(**config)
    data_source_loading_pipeline(config)
