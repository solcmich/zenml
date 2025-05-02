make init

source .venv/bin/activate

make create-components-local_docker
make register-stack-local_docker

make run-pipeline-local_docker
make run-pipeline-local_docker PIPELINE=monitoring_pipeline
make run-pipeline-local_docker PIPELINE=data_source_loading_pipeline

make create-components-local_docker ENV=prod
make register-stack-local_docker ENV=prod

make run-pipeline-local_docker ENV=prod
make run-pipeline-local_docker PIPELINE=monitoring_pipeline ENV=prod
make run-pipeline-local_docker PIPELINE=data_source_loading_pipeline ENV=prod