import logging
import time
import numpy as np
import mlflow
import os
from zenml import step
from zenml.config import DockerSettings
from pipelines.config import TrainingPipelineConfig
import pandas as pd

logger = logging.getLogger(__name__)

class MockModel:
    """A simple mock model that returns random predictions."""
    def __init__(self, station_id: str, model_params: dict):
        self.station_id = station_id
        self.model_params = model_params
        self.coefficients = np.random.rand(4)  # Random coefficients for features
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generate mock predictions."""
        return np.dot(X, self.coefficients) + np.random.normal(0, 1, len(X))

ENV = os.environ["LWF_ENV"]
STACK = os.environ["LWF_STACK"]

print(os.environ["LWF_STACK"])

@step(
    settings={
        "docker": DockerSettings(
            parent_image="zenmldocker/zenml:py3.11",
            replicate_local_python_environment="pip_freeze",
        ),
    },
    experiment_tracker=f"{STACK}_tracker_{ENV}",
)
def train_models(
    training_data: dict[str, pd.DataFrame],
    config: TrainingPipelineConfig,
) -> dict:
    """Mock version: Train simple models for each station and log to MLflow.
    
    Args:
        training_data: Training data (not used in mock)
        config: Pipeline configuration
        
    Returns:
        dict: Dictionary of trained models by station
    """
    logger.info("Mock: Starting model training...")
    time.sleep(2)  # Simulate training time
    
    # Create mock models for each station
    stations = ['station1', 'station2', 'station3']
    models = {}
    
    for station in stations:
        logger.info(f"Mock: Training model for station {station}")
        
        # Generate random model parameters
        model_params = {
            'learning_rate': np.random.uniform(0.001, 0.01),
            'batch_size': np.random.choice([32, 64, 128]),
            'hidden_size': np.random.choice([64, 128, 256]),
            'dropout': np.random.uniform(0.1, 0.5),
            'optimizer': np.random.choice(['adam', 'sgd', 'rmsprop'])
        }
        
        # Start MLflow run for this station
        with mlflow.start_run(run_name=f"{station}", nested=True):
            # Log parameters
            mlflow.log_params({
                'station_id': station,
                **model_params
            })
            
            # Generate and log random metrics
            metrics = {
                'train_loss': np.random.uniform(0.1, 0.5),
                'val_loss': np.random.uniform(0.15, 0.6),
                'train_mae': np.random.uniform(0.5, 2.0),
                'val_mae': np.random.uniform(0.6, 2.5),
                'train_r2': np.random.uniform(0.7, 0.95),
                'val_r2': np.random.uniform(0.65, 0.9)
            }
            mlflow.log_metrics(metrics)
            
            # Log some artifacts (mock model weights)
            weights = {
                'coefficients': np.random.rand(4).tolist(),
                'bias': np.random.randn()
            }
            mlflow.log_dict(weights, "model_weights.json")
            
            # Log tags
            mlflow.set_tags({
                'model_type': 'mock_transformer',
                'data_source': 'synthetic',
                'environment': "mock"
            })
            
            # Create and store the model
            model = MockModel(station, model_params)
            models[station] = model
            
            logger.info(f"Mock: Logged experiment for station {station}")
    
    logger.info("Mock: Model training and MLflow logging completed")
    return models 