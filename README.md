# ZenML productionalization template

This directory contains the core pipeline system for the Weather Prediction project. The system is built using ZenML and consists of three main pipelines: data loading, training, and monitoring.

## Pipeline Architecture

The system follows a modular design with three main pipelines:

1. **Data Source Loading Pipeline** (`data_source_loading_pipeline.py`)
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

## Repository Structure

```
template/
├── docker/               # Docker orchestration of MLflow and inference server
├── pipelines/            # Pipelines
├── forecasting.py        # Sample forecasting service
├── tests/                # scripts for testing
├── requirements.txt      # Requirements
├── .env.example          # Env example
└── Makefile/             # Orchestartion and abstraction
```

## Pipelines Structure

```
pipelines/
├── config.py             # Central configuration management
├── run.py                # Pipeline execution entry point
├── data_source_loading_pipeline.py
├── training_pipeline.py
├── monitoring_pipeline.py
├── configs/              # YAML configuration files
└── steps/                # Mock implementations for testing
```



## Configuration

The system uses YAML-based configuration files located in the `configs/` directory. Each pipeline has its own configuration file:

- `data_source_loading.yaml`: Data source and loading parameters
- `training.yaml`: Model training and validation settings
- `monitoring.yaml`: Monitoring and drift detection parameters

## Environment Setup

The system supports multiple environments (dev/prod) with environment-specific settings:

```bash
export ENV=dev  # or test,prod
export STACK=local  # or local_docker
```

# How to run

To run the Pipeline System, follow these steps (for the weather use case pipeline system, the steps are the same, just every environmental variable has a prefix `LWF_`):

1. **Prerequisites:**
   - Docker daemon is running.
   - If you have any docker registries that require authentication in the docker config, you need to be authenticated.
   - Python is installed.

2. **Set up the environment:**

   ```bash
   # Install all requirements and run ZenML server as follows:
   make init

   # Activate venv:
   source .venv/bin/activate

   # Create ZenML components:
   make create-components-{local, local_docker} ENV={dev,test,prod}

   # Register ZenML stacks:
   make register-stack-{local, local_docker} ENV={dev,test,prod}
   ```

3. **Run MLflow server:**

   Run MLflow and prediction server using the predefined docker compose.

   ```bash
   # Run MLflow server in separate bash
   make run-mlflow
   ```

4. **Execute the pipelines:**

   Pipelines are executed via a `Makefile` interface. Run specific pipelines using:

   ```bash
   # Run the data loading pipeline
   make run-pipeline-{local, local_docker} PIPELINE=data_source_loading_pipeline ENV={dev,test,prod}

   # Run the training pipeline (default)
   make run-pipeline-{local, local_docker} PIPELINE=training_pipeline ENV={dev,test,prod}

   # Run the monitoring pipeline
   make run-pipeline-{local, local_docker} PIPELINE=monitoring_pipeline ENV={dev,test,prod}
   ```

5. **Configuration:**
   - Configuration files located in the `configs/` directory define parameters for each pipeline:
     - `data_loading.yaml` for data ingestion settings
     - `training.yaml` for model training parameters
     - `monitoring.yaml` for monitoring and drift detection

6. **MLflow Integration:**

   Ensure MLflow is running (e.g., via `docker-compose` in the `../docker` directory) for experiment tracking, model versioning, and model registry management.

7. **Run predictions:**

   If training was already run and some models are registered, you can run test predictions using:

   ```bash
   python tests/predict_test.py
   ```
# How to test
For testing, you can run the test scripts in tests folder

   ```bash
   ./tests/tests_local.sh
   ./tests/tests_docker.sh
   ./tests/test_mlflow.sh
   python predict_test.py
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