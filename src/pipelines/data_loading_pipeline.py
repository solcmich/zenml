from zenml import pipeline
from typing import Optional
from pipelines.config import DataLoadingPipelineConfig
from pipelines.mockup_steps.data_source_loader import load_data_sources

@pipeline(enable_cache=False)
def data_loading_pipeline(
    config: DataLoadingPipelineConfig
) -> None:
    """Pipeline for loading data from various sources.
    """
    # Load data from sources
    load_data_sources(config) 

def run(config: dict, env: str):
    """Run the data loading pipeline with configuration from YAML.
    
    Args:
        config: Dictionary containing pipeline configuration loaded from YAML
        env: Environment name (dev/prod)
    """
    # Run the pipeline with configuration from YAML
    cfg = DataLoadingPipelineConfig(**config)
    data_loading_pipeline(
        cfg
    )