ifneq (,$(wildcard .env))
    include .env
    export
endif

SHELL := /bin/bash

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
	@echo "  clean          - Clean up temporary files and caches"
	@echo "  help           - Show this help message"


init: 
	@python -m venv .venv && \
	echo "export PYTHONPATH=\"$$PWD/src/pipelines/\"" >> .venv/bin/activate && \
	. .venv/bin/activate && \
	pip install -r requirements.txt && \
	zenml login --local --docker

# Generic component creation target
create-components-%:
	@echo "Creating $* stack components..."
	@zenml orchestrator register $*_orchestrator_$(ENV) --flavor=$*
	@zenml artifact-store register $*_store_$(ENV) --flavor=local
	@{ \
		if [ "$*" = "local_docker" ]; then \
			uri="http://host.docker.internal:5050"; \
		else \
			uri="$(MLFLOW_TRACKING_URL)"; \
		fi; \
		echo "Using tracking URI: $$uri"; \
		zenml experiment-tracker register $*_tracker_$(ENV) --flavor=mlflow \
			--tracking_uri=$$uri --tracking_username=admin --tracking_password=admin; \
	}


# Generic component creation target
delete-components-%:
	@echo "Creating $* stack components..."
	@zenml orchestrator delete $*_orchestrator_$(ENV)
	@zenml artifact-store delete $*_store_$(ENV)
	@zenml experiment-tracker delete $*_tracker_$(ENV)


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
	@zenml stack set $*_stack_$(ENV)

run-mlflow: 
	@echo "Starting mlflow and forecasting server on $(MLFLOW_TRACKING_URL)"
	@cd docker && docker-compose up

run-pipeline-%: 
	@echo "Running pipeline $(PIPELINE) with stack $* in environment $(ENV)"
	@cd src && \
	export STACK=$* && \
	zenml stack set $*_stack_$(ENV) && \
	python pipelines/run.py

clean:
	@echo "Cleaning up..."
	@zenml clean
	@rm -rf __pycache__
	@rm -rf .pytest_cache
	@rm -rf storage/

