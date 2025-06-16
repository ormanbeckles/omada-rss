import requests

class Omada:
    def __init__(self, baseurl, site, username, password, verify=True):
        self.baseurl = baseurl.rstrip('/')
        self.site = site
        self.username = username
        self.password = password
        self.verify = verify
        self.token = None
        self.session = requests.Session()

    def login(self):
        url = f"{self.baseurl}/api/v2/login"
        payload = {
            "username": self.username,
            "password": self.password
        }
        headers = {"Content-Type": "application/json"}

        response = self.session.post(url, json=payload, headers=headers, verify=self.verify)
        response.raise_for_status()
        data = response.json()

        if data.get("errorCode", 0) != 0:
            raise Exception(f"Login failed: {data.get('msg', 'Unknown error')}")

        self.token = data["result"]["token"]
        self.session.headers.update({
            "Csrf-Token": self.token
        })

    def get_clients(self):
        url = f"{self.baseurl}/api/v2/sites/{self.site}/clients"
        response = self.session.get(url, verify=self.verify)
        response.raise_for_status()
        data = response.json()

        if data.get("errorCode", 0) != 0:
            raise Exception(f"Failed to get clients: {data.get('msg', 'Unknown error')}")

        return data["result"]["data"]
