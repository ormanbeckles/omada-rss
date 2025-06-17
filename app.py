from flask import Flask, jsonify, request
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
    print("🔐 Attempting login...")
    resp = requests.post(OMADA_API_LOGIN, json={'username': USERNAME, 'password': PASSWORD})
    print(f"📥 Login status: {resp.status_code}")
    print("Headers:", resp.headers)
    print("Cookies:", resp.cookies.get_dict())
    print("Body:", resp.text)

    try:
        data = resp.json()
    except Exception as e:
        print("❌ JSON parse error:", str(e), resp.text)
        return None, None

    token = data.get('result', {}).get('token')
    cookie = resp.cookies.get('TOKEN')
    print("Parsed token:", token)
    print("Parsed TOKEN cookie:", cookie)
    return token, cookie

def get_controller_status(token, cookie, location_name):
    headers = {'Csrf-Token': token}
    cookies = {'TOKEN': cookie}
    print("➡️ Fetching controllers with headers:", headers, "and cookies:", cookies)
    resp = requests.get(OMADA_API_CONTROLLERS, headers=headers, cookies=cookies)
    print("📥 Controllers status:", resp.status_code)
    print("Body:", resp.text)
    try:
        data = resp.json()
    except Exception as e:
        print("❌ JSON parse error on controllers:", str(e), resp.text)
        return None

    controllers = data.get('result', {}).get('controllers', [])
    matched = next((c for c in controllers if c.get('name') == location_name), None)
    print("Controllers list:", controllers)
    if matched:
        status = 'online' if matched.get('status') == 1 else 'offline'
        print(f"🎯 Matched '{location_name}' status:", status)
        return status

    print(f"⚠️ No match found for '{location_name}'")
    return 'not found'

@app.route('/get-asgard-status', methods=['GET'])
def get_asgard_status():
    token, cookie = login()
    if not token or not cookie:
        return jsonify({'status': 'error', 'message': 'Login failed', 'token': token, 'cookie': cookie}), 500

    status = get_controller_status(token, cookie, TARGET_LOCATION)
    if not status:
        return jsonify({'status': 'error', 'message': 'Failed to fetch controllers'}), 500

    return jsonify({TARGET_LOCATION: status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
