ifneq (,$(wildcard .env))
    include .env
    export
endif

.PHONY: init init-local init-docker run-pipeline run-prediction-service clean help test

ENV ?= dev
STACK ?= local
PIPELINE ?= training_pipeline
MLFLOW_TRACKING_URL ?= http://127.0.0.1:5050

help:
	@echo "Available targets:"
	@echo "  init           - Initialize the project with specified environment (LWF_ENV=dev|prod)"
	@echo "  init-local     - Initialize local stack"
	@echo "  init-docker    - Initialize docker stack"
	@echo "  run            - Run pipeline with specified stack and environment"
	@echo "  clean          - Clean up temporary files and caches"
	@echo "  help           - Show this help message"

init: check-requirements
	@python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && zenml login --local --docker

check-requirements:
	@echo "Checking requirements..."
	@pip install -r requirements.txt
	@pip install zenml

# Generic component creation target
create-components-%:
	@echo "Creating $(*) stack components..."
	@zenml orchestrator register $*_orchestrator_$(ENV) --flavor=$(*)
	@zenml artifact-store register $*_store_$(ENV) --flavor=local
	@zenml experiment-tracker register $*_tracker_$(ENV) --flavor=mlflow --tracking_uri=$(MLFLOW_TRACKING_URL) --tracking_username=admin --tracking_password=admin

# Generic stack registration target
register-stack-%:
	@echo "Registering $* stack..."
	@zenml stack register $*_stack_$(ENV) \
		-o $*_orchestrator_$(ENV) \
		-a $*_store_$(ENV) \
		-e $*_tracker_$(ENV) \
		--set

set-stack-%:
	@echo "Setting $* stack as active stack.."
	@zenml stack set $*_stack_$(ENV) \

run-pipeline-%:
	@echo "Running pipeline $(PIPELINE) with stack $* in environment $(ENV)"
	@cd src/ && zenml stack set $*_stack_$(ENV)
	@cd src/ && python pipelines/run.py

run-prediction-service:
	@cd src/ && python ai_weather_forecasting_service/main.py

test:
	@@cd src/ && python pipelines/tests/pipelines/test_validation_deployment.py

clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__
	@rm -rf .pytest_cache

