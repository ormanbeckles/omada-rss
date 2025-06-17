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
    print(f"🔐 Payload (username only): {{'username': '{USERNAME}', 'password': '***'}}")
    try:
        response = requests.post(OMADA_API_LOGIN, json=payload, headers=headers)
        print(f"🔄 Login response status: {response.status_code}")

        if response.status_code != 200:
            print("❌ Login failed — Non-200 status")
            print("❌ Response text:", response.text)
            return None

        try:
            data = response.json()
            print("✅ Login JSON parsed:", data)
            return data.get('result', {}).get('token')
        except Exception as e:
            print("❌ Failed to parse login response as JSON")
