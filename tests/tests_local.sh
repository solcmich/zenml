#!/bin/bash

make init

source .venv/bin/activate

make create-components-local

make register-stack-local

make run-pipeline-local

make run-pipeline-local PIPELINE=monitoring_pipeline
make run-pipeline-local PIPELINE=data_source_loading_pipeline

make create-components-local ENV=prod

make register-stack-local ENV=prod

make run-pipeline-local ENV=prod

make run-pipeline-local PIPELINE=monitoring_pipeline ENV=prod
make run-pipeline-local PIPELINE=data_source_loading_pipeline ENV=prod
