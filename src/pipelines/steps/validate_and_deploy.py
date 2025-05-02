import logging
import time
import numpy as np
import mlflow
import os
from zenml import step
from zenml.config import DockerSettings
from config import TrainingPipelineConfig
from mlflow.tracking import MlflowClient
import random

logger = logging.getLogger(__name__)

ENV = os.environ["ENV"]
STACK = os.environ["STACK"]


def get_run_by_name(parent_run_id: str, station_id: str):
    """Helper to retrieve child run matching station ID."""
    client = MlflowClient()
    run = client.get_run(parent_run_id)
    child_runs = client.search_runs(
        [run.info.experiment_id],
        f"tags.mlflow.parentRunId = '{parent_run_id}' and tags.mlflow.runName = '{station_id}'",
    )
    return child_runs[0] if child_runs else None


def is_challenger_better(client: MlflowClient, station_id: str, parent_run_id: str):
    """Implement custom method to evaluate champion vs. challenger."""
    challenger_info = client.get_model_version_by_alias(station_id, "challenger")
    try:
        champion_info = client.get_model_version_by_alias(station_id, "champion")
    except:
        logging.info("No champion found, promoting challenger.")
        return True

    # logic for comparsion
    return random.choice([True, False])


def promote_challenger_to_champion(
    client: MlflowClient, station_id: str, parent_run_id: str
) -> None:
    challenger_run = get_run_by_name(parent_run_id, station_id)
    if not challenger_run:
        logger.warning(
            f"No challenger run found for station {station_id}. Cannot promote."
        )
        return

    registered_models = client.search_model_versions(f"name='{station_id}'")

    logger.info(f"Promoting the last version of the model to champion.")
    client.set_registered_model_alias(
        name=station_id,
        version=str(len(registered_models)),
        alias="champion",
    )


@step(
    settings={
        "docker": DockerSettings(
            parent_image="zenmldocker/zenml:0.82.0-py3.11",
            replicate_local_python_environment="pip_freeze",
            environment={"ENV": ENV, "STACK": STACK}
        ),
    },
    experiment_tracker=f"{STACK}_tracker_{ENV}",
)
def validate_and_deploy_models(
    trained_models: dict, config: TrainingPipelineConfig
) -> None:
    """Register trained models and promote challengers to champions if available."""
    logger.info("Starting model registration and promotion...")

    client = MlflowClient()
    parent_run_id = mlflow.active_run().info.run_id

    for station_id, _ in trained_models.items():
        try:
            model_name = station_id

            filter_string = (
                f"tags.mlflow.parentRunId = '{parent_run_id}' and "
                f"attribute.run_name = '{station_id}'"
            )

            # Register model
            run_ids = mlflow.search_runs(filter_string=filter_string, output_format="list")
            run_id = run_ids[0].info.run_id

            model_uri = f"runs:/{run_id}/model"
            registered_model = mlflow.register_model(
                model_uri=model_uri, name=model_name
            )
            latest_versions = client.get_latest_versions(model_name)
            latest_version = max(latest_versions, key=lambda v: int(v.version))
            client.set_registered_model_alias(
                model_name, version=str(latest_version.version), alias="challenger"
            )
            logger.info(
                f"Registered model {model_name} version {registered_model.version}"
            )

            if is_challenger_better(client, station_id, parent_run_id):
                promote_challenger_to_champion(client, station_id, parent_run_id)

            client.delete_registered_model_alias(model_name, "challenger")

        except Exception as e:
            logger.error(f"Failed for station {station_id}: {str(e)}")
            continue

    logger.info("Model registration and promotion completed.")
