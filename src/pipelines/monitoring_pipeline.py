import os
from mockup_steps.monitor import generate_evidently_report

from zenml import pipeline
from zenml.config import DockerSettings

from pipelines.config import MonitoringConfig

ENV = os.environ["ENV"]
STACK = os.environ["STACK"]


# Either add it to the decorator
@pipeline(
    settings={
        "docker": DockerSettings(
            parent_image="zenmldocker/zenml:py3.11",
            # replicate_local_python_environment="pip_freeze",
        ),
    },
    enable_cache=False,
    name=f"monitoring_pipeline_{ENV}",
)
def monitoring_pipeline(cfg: MonitoringConfig):
    generate_evidently_report(cfg)


def run(config: dict, env: str):
    """Run the monitoring pipeline with configuration from YAML.

    Args:
        config: Dictionary containing pipeline configuration loaded from YAML
        env: Environment name (dev/prod)

    """
    paths_config = config.get("paths", {})

    # Create monitoring config
    cfg = MonitoringConfig(
        log_dir=paths_config.get("log_dir", "../storage/forecasts_evidently/"),
        reference_data_dir=paths_config.get(
            "reference_data_dir", "../src/example_fs_station_database",
        ),
    )

    # Run the pipeline
    monitoring_pipeline(cfg)
