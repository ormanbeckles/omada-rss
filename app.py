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
    try:
        response = requests.post(OMADA_API_LOGIN, json=payload, headers=headers)
        print(f"🔄 Login response status: {response.status_code}")
        print("🔍 Raw login response text:", response.text)

        if response.status_code != 200:
            return None, None

        try:
            data = response.json()
        except Exception as e:
            print("❌ Could not parse JSON:", e)
            print("❌ Login raw response (unparsed):", response.text)
            return None, None

        token = data.get('result', {}).get('token')
        cookie = response.cookies.get('TOKEN')
        print("✅ Token:", token)
        print("✅ TOKEN Cookie:", cookie)
        return token, cookie

    except Exception as e:
        print("❌ Exception during login:", e)
        return None, None


def get_controller_status(token, cookie, location_name):
    headers = {'Csrf-Token': token}
    cookies = {'TOKEN': cookie}

    print(f"📡 Fetching controllers from {OMADA_API_CONTROLLERS}")
    try:
        response = requests.get(OMADA_API_CONTROLLERS, headers=headers, cookies=cookies)
        print(f"🔄 Controller fetch status: {response.status_code}")
        print("🔍 Controller response:", response.text)

        if response.status_code != 200:
            return 'API Error'

        try:
            data = response.json()
        except Exception as e:
            print("❌ JSON parse failed on controller response:", e)
            return 'error'

        controllers = data.get('result', {}).get('controllers', [])
        print("✅ Controllers:", [c['name'] for c in controllers])

        matched = next((c for c in controllers if c['name'] == location_name), None)
        if matched:
            status = 'online' if matched.get('status') == 1 else 'offline'
            print(f"🎯 '{location_name}' matched, status:", status)
            return status

        print(f"⚠️ No controller matched: {location_name}")
        return 'not found'

    except Exception as e:
        print("❌ Exception during controller fetch:", e)
        return 'error'


@app.route('/get-asgard-status')
def get_asgard_status():
    print("🚦 Handling request: /get-asgard-status")
    token, cookie = login()
    if not token or not cookie:
        print("🚫 Login failed or session missing.")
        return jsonify({'status': 'error', 'message': 'Login failed'}), 500

    status = get_controller_status(token, cookie, TARGET_LOCATION)
    return jsonify({TARGET_LOCATION: status})


@app.route('/debug-login-response')
def debug_login_response():
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    payload = {"username": USERNAME, "password": PASSWORD}

    try:
        response = requests.post(OMADA_API_LOGIN, json=payload, headers=headers)
        return response.text, response.status_code, {'Content-Type': response.headers.get('Content-Type', 'text/plain')}
    except Exception as e:
        return f"Login Exception: {e}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
