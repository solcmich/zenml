ifneq (,$(wildcard .env))
    include .env
    export
endif

.PHONY: init init-local init-docker run-pipeline run-prediction-service clean help test

LWF_ENV ?= dev
LWF_STACK ?= local
LWF_PIPELINE ?= training_pipeline
LWF_MOCKUP ?= False

help:
	@echo "Available targets:"
	@echo "  init           - Initialize the project with specified environment (LWF_ENV=dev|prod)"
	@echo "  init-local     - Initialize local stack"
	@echo "  init-docker    - Initialize docker stack"
	@echo "  run            - Run pipeline with specified stack and environment"
	@echo "  clean          - Clean up temporary files and caches"
	@echo "  help           - Show this help message"

init: check-requirements
	@export DOCKER_HOST=unix:///Users/solcmich/.colima/default/docker.sock
	@zenml login --local --docker

check-requirements:
	@echo "Checking requirements..."
	@pip install -r requirements.txt
	@pip install zenml

# Generic component creation target
create-components-%:
	@echo "Creating $(*) stack components..."
	@zenml orchestrator register $*_orchestrator_$(LWF_ENV) --flavor=$(*)
	@zenml artifact-store register $*_store_$(LWF_ENV) --flavor=local
	@zenml experiment-tracker register $*_tracker_$(LWF_ENV) --flavor=mlflow

# Generic stack registration target
register-stack-%:
	@echo "Registering $* stack..."
	@zenml stack register $*_stack_$(LWF_ENV) \
		-o $*_orchestrator_$(LWF_ENV) \
		-a $*_store_$(LWF_ENV) \
		-e $*_tracker_$(LWF_ENV) \
		--set

set-stack-%:
	@echo "Setting $* stack as active stack.."
	@zenml stack set $*_stack_$(LWF_ENV) \

run-pipeline:
	@echo "Running pipeline $(LWF_PIPELINE) with stack $(LWF_STACK) in environment $(LWF_ENV)"
	@cd src/ && zenml stack set $(LWF_STACK)_stack_$(LWF_ENV)
	@cd src/ && python pipelines/run.py

run-prediction-service:
	@cd src/ && python ai_weather_forecasting_service/main.py

test:
	@@cd src/ && python pipelines/tests/pipelines/test_validation_deployment.py

clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__
	@rm -rf .pytest_cache

