import requests

# URL of the FastAPI endpoint
url = "http://localhost:8000/predict"

# Example feature data (must match expected input shape)
payload = {
    "features": [
        [0.1, 0.2, 0.3, 0.4],
        [0.5, 0.6, 0.7, 0.8]
    ]
}

# Make POST request
response = requests.post(url, json=payload)

# Handle response
if response.status_code == 200:
    print("Predictions:", response.json()["predictions"])
else:
    print("Error:", response.status_code, response.text)