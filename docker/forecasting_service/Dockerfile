# Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ src/

ENV PYTHONPATH=src/pipelines/

ENV MLFLOW_MODEL_URI=models:/station1@champion

EXPOSE 8000

CMD ["uvicorn", "src.forecasting:app", "--host", "0.0.0.0", "--port", "8000"]