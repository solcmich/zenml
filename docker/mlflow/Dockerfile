FROM ghcr.io/mlflow/mlflow:v2.17.2
LABEL authors="cepekmir"

RUN mkdir -p /var/mlflow/

EXPOSE 5050
ENV LWF_MLFLOW_TRACKING_URI="file:///var/mlflow/tracking"
ENV LWF_MLFLOW_ARTIFACT_DESTINATION="file:///var/mlflow/artifacts"
# ENV MLFLOW_FLASK_SERVER_SECRET_KEY="my-secret-key"
VOLUME /var/mlflow/

CMD  ["sh", "-c", "mlflow server --port 5050 --host 0.0.0.0 --backend-store-uri ${LWF_MLFLOW_TRACKING_URI} --artifacts-destination ${LWF_MLFLOW_ARTIFACT_DESTINATION}"]
