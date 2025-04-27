from zenml import pipeline
from typing import Optional
from pipelines.config import DataLoadingPipelineConfig
from pipelines.mockup_steps.data_source_loader import load_data_sources

@pipeline(enable_cache=False)
def data_loading_pipeline(
    data_source_id: Optional[str] = None,
    new_source_history_length_days: int = 100,
    force_full_history_download: bool = True,
    source_update_cooldown_minutes: int = 30,
    parallel_downloads: int = 1,
) -> None:
    """Pipeline for loading data from various sources.
    
    This pipeline:
    1. Loads data from configured data sources (GFS, EkoVin, Vitispector)
    2. Handles data validation and preprocessing
    3. Stores the data in the configured storage system
    
    Args:
        data_source_id: ID of data source to download. Can use wildcard * to download multiple
        new_source_history_length_days: Number of days of history to download for new sources
        force_full_history_download: Force download of full history even if data exists
        source_update_cooldown_minutes: Cooldown time in minutes before updating a source
        parallel_downloads: Number of parallel downloads to run
    """
    # Create config with the provided parameters
    config = DataLoadingPipelineConfig(
        data_source_id=data_source_id,
        new_source_history_length_days=new_source_history_length_days,
        force_full_history_download=force_full_history_download,
        source_update_cooldown_minutes=source_update_cooldown_minutes,
        parallel_downloads=parallel_downloads,
    )
    
    # Load data from sources
    load_data_sources(config) 

def run(config: dict, env: str):
    """Run the data loading pipeline with configuration from YAML.
    
    Args:
        config: Dictionary containing pipeline configuration loaded from YAML
        env: Environment name (dev/prod)
    """
    data_source_config = config.get('data_source', {})
    
    # Run the pipeline with configuration from YAML
    data_loading_pipeline(
        data_source_id=data_source_config.get('id', '*'),
        new_source_history_length_days=data_source_config.get('new_source_history_length_days', 100),
        force_full_history_download=data_source_config.get('force_full_history_download', True),
        source_update_cooldown_minutes=data_source_config.get('source_update_cooldown_minutes', 30),
        parallel_downloads=data_source_config.get('parallel_downloads', 1)
    )