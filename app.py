from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OMADA_API_LOGIN = 'https://use1-api-omada-central.tplinkcloud.com/api/v2/login'
OMADA_API_CONTROLLERS = 'https://use1-api-omada-central.tplinkcloud.com/api/v2/controllers'

USERNAME = 'orman@asgardx.com'
PASSWORD = 'fGss8FWx2K6Fr*uP'
TARGET_LOCATION = 'Asgard'

def login():
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }

    print(f"🔐 Attempting login to {OMADA_API_LOGIN}")
    print(f"🔐 Payload: {{'username': '{USERNAME}', 'password': '***'}}")
    
    try:
        response = requests.post(OMADA_API_LOGIN, json=payload, headers=headers)
        print(f"🔄 Login response status: {response.status_code}")
        print(f"🔍 Raw response text:\n{response.text[:500]}")  # log first 500 chars max

        if response.status_code != 200:
            print("❌ Login failed: status not 200")
            return None

        try:
            data = response.json()
        except Exception as json_error:
            print("❌ JSON parse failed:", json_error)
            print("🧾 Raw content looked like:\n", response.text[:500])
            return None

        print("✅ Parsed login JSON:", data)
        return data.get('result', {}).get('
