import requests
import json

# API endpoint
url = "http://127.0.0.1:8000/analyze-risk"

# Scenario to analyze
payload = {
    "scenario": "Supply chain disruption due to port strikes"
}

# Set headers
headers = {
    "Content-Type": "application/json"
}

# Make POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Check response
if response.status_code == 200:
    result = response.json()
    print("Scenario:", result["scenario"])
    print("Risk Analysis:\n", result["risk_analysis"])
else:
    print("Error:", response.status_code, response.text)
