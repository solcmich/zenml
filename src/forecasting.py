# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import numpy as np
import os

class MockPyFuncWrapper: # mock the model here
    def __init__(self):
        # Generate random coefficients and bias every time model is loaded
        self.coefficients = np.random.rand(4)
        self.bias = np.random.randn()

    def predict(self, model_input):
        return np.dot(model_input, self.coefficients) + self.bias

# Load model from MLflow
mlflow.set_tracking_uri("http://mlflow:5050")
MLFLOW_MODEL_URI = os.getenv("MLFLOW_MODEL_URI", "models:/station1@champion")

# Define input format
class ForecastRequest(BaseModel):
    features: list[list[float]]  # 2D list: batch of feature vectors

app = FastAPI()

@app.post("/predict")
def predict(request: ForecastRequest):
    model = MockPyFuncWrapper() # tba: load real mlflow model mlflow.pyfonc.load_model(MLFLOW_MODEL_URI)
    try:
        X = np.array(request.features)
        preds = model.predict(X)
        # todo: also import traffic saving logic here.
        return {"predictions": preds.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
