import os
from steps.monitor import generate_evidently_report

from zenml import pipeline
from zenml.config import DockerSettings

from config import MonitoringConfig

ENV = os.environ["ENV"]
STACK = os.environ["STACK"]


# Either add it to the decorator
@pipeline(
    settings={
        "docker": DockerSettings(
            parent_image="zenmldocker/zenml:py3.11",
            # replicate_local_python_environment="pip_freeze",
            environment={"ENV": ENV, "STACK": STACK}
        ),
    },
    enable_cache=False,
    name=f"{STACK}_monitoring_pipeline_{ENV}",
)
def monitoring_pipeline(cfg: MonitoringConfig):
    """Monitoring pipeline example

    Parameters
    ----------
    cfg : MonitoringConfig
        Config to pass to the monitoring pipeline
    """
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
        log_dir=paths_config.get("log_dir", "../storage/forecasts/"),
        reference_data_dir=paths_config.get(
            "reference_data_dir", "../src/reference_data",
        ),
    )

    # Run the pipeline
    monitoring_pipeline(cfg)
