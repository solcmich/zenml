# Weather Prediction Pipeline System

This directory contains the core pipeline system for the Weather Prediction project. The system is built using ZenML and consists of three main pipelines: data loading, training, and monitoring.

## Pipeline Architecture

The system follows a modular design with three main pipelines:

1. **Data Loading Pipeline** (`data_loading_pipeline.py`)
   - Handles data ingestion from various sources
   - Manages data updates and cooldown periods
   - Supports parallel processing for efficient data loading

2. **Training Pipeline** (`training_pipeline.py`)
   - Manages model training and validation
   - Integrates with MLflow for experiment tracking
   - Handles model versioning and registry

3. **Monitoring Pipeline** (`monitoring_pipeline.py`)
   - Tracks data and model drift
   - Generates Evidently reports
   - Monitors model performance

## Directory Structure

```
pipelines/
├── config.py              # Central configuration management
├── run.py                # Pipeline execution entry point
├── data_loading_pipeline.py
├── training_pipeline.py
├── monitoring_pipeline.py
├── configs/              # YAML configuration files
└── mockup_steps/        # Mock implementations for testing
```

## Configuration

The system uses YAML-based configuration files located in the `configs/` directory. Each pipeline has its own configuration file:

- `data_loading.yaml`: Data source and loading parameters
- `training.yaml`: Model training and validation settings
- `monitoring.yaml`: Monitoring and drift detection parameters

## Environment Setup

The system supports multiple environments (dev/prod) with environment-specific settings:

```bash
export ENV=dev  # or test,prod
export STACK=local  # or docker
```

## Running Pipelines

Pipelines can be executed using the `makefile`:

```bash
# Run data loading pipeline
make run-pipeline-local PIPELINE=data_loading_pipeline

# Run training pipeline
make run-pipeline-local PIPELINE=training_pipeline # (default)

# Run monitoring pipeline
make run-pipeline-local PIPELINE=monitoring_pipeline
```

## Mockup Steps

The `mockup_steps/` directory contains simplified implementations of pipeline steps for testing:

- `data_loader.py`: Mock data loading
- `trainer.py`: Mock model training
- `validate_and_deploy.py`: Mock validation and deployment
- `monitor.py`: Mock monitoring with Evidently

## MLflow Integration

The system integrates with MLflow for:
- Experiment tracking
- Model versioning
- Model registry
- Champion/challenger model management

## Monitoring and Reporting

The monitoring pipeline generates Evidently reports that include:
- Data drift detection
- Model performance metrics
- Data quality monitoring
- Feature distribution analysis

## Development Guidelines

1. **Adding New Steps**
   - Create new step in appropriate directory
   - Add step to pipeline configuration
   - Update pipeline implementation

2. **Modifying Pipelines**
   - Update YAML configuration
   - Modify pipeline implementation
   - Update documentation

3. **Testing**
   - Use mockup steps for development
   - Test with different configurations
   - Verify MLflow integration

## Troubleshooting

Common issues and solutions:

1. **Pipeline Execution**
   - Check environment variables
   - Verify configuration files
   - Check MLflow connection

2. **Data Loading**
   - Verify data source connections
   - Check cooldown periods
   - Validate data formats

3. **Model Training**
   - Check MLflow connection (started via docker-compose in `../docker`)
   - Verify model registry access
   - Monitor resource usage
