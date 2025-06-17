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
            print("❌ Raw response text:", response.text)
            return None

    except Exception as e:
        print(f"❌ Exception during login: {e}")
        return None

def get_controller_status(token, location_name):
    headers = {'Csrf-Token': token}
    cookies = {'TOKEN': token}

    print(f"📡 Fetching controllers from {OMADA_API_CONTROLLERS}")
    try:
        response = requests.get(OMADA_API_CONTROLLERS, headers=headers, cookies=cookies)
        print(f"🔄 Controller fetch status: {response.status_code}")

        if response.status_code != 200:
            print("❌ Controller fetch failed — Non-200 status")
            print("❌ Response text:", response.text)
            return 'API Error'

        try:
            data = response.json()
            controllers = data.get('result', {}).get('controllers', [])
            print("✅ Controllers found:", [c['name'] for c in controllers])

            matched = next((c for c in controllers if c['name'] == location_name), None)
            if matched:
                print(f"🎯 Matched controller '{location_name}' — status:", matched.get('status'))
                return 'online' if matched.get('status') == 1 else 'offline'

            print(f"⚠️ No matching controller named '{location_name}' found.")
            return 'offline'

        except Exception as e:
            print("❌ Failed to parse controller response as JSON")
            print("❌ Raw response text:", response.text)
            return 'error'

    except Exception as e:
        print(f"❌ Exception during controller fetch: {e}")
        return 'error'

@app.route('/get-asgard-status')
def get_asgard_status():
    print("🚦 Handling request: /get-asgard-status")
    token = login()
    if not token:
        print("🚫 Login returned no token.")
        return jsonify({'status': 'error', 'message': 'Login failed'})
    
    status = get_controller_status(token, TARGET_LOCATION)
    print(f"📦 Final status returned: {TARGET_LOCATION} → {status}")
    return jsonify({TARGET_LOCATION: status})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
