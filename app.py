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
    response = requests.post(OMADA_API_LOGIN, json={
        'username': USERNAME,
        'password': PASSWORD
    })
    if response.status_code != 200:
        return None
    data = response.json()
    return data.get('result', {}).get('token')

def get_controller_status(token, location_name):
    headers = {'Csrf-Token': token}
    cookies = {'TOKEN': token}
    response = requests.get(OMADA_API_CONTROLLERS, headers=headers, cookies=cookies)
    if response.status_code != 200:
        return 'API Error'
    data = response.json()
    controllers = data.get('result', {}).get('controllers', [])
    matched = next((c for c in controllers if c['name'] == location_name), None)
    if matched:
        return 'online' if matched.get('status') == 1 else 'offline'
    return 'offline'

@app.route('/get-asgard-status')
def get_asgard_status():
    token = login()
    if not token:
        return jsonify({'status': 'error', 'message': 'Login failed'})
    status = get_controller_status(token, TARGET_LOCATION)
    return jsonify({TARGET_LOCATION: status})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
