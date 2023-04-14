import requests

class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiration_time = None
        self.token_type = None

    def get_access_token(self):
        if self.access_token is not None and self.token_expiration_time is not None:
            if self.token_expiration_time > datetime.now():
                return self.access_token
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}"
        }
        
        data = {
            "grant_type": "client_credentials"
        }
        
        response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            self.token_type = data["token_type"]
            self.token_expiration_time = datetime.now() + timedelta(seconds=data["expires_in"])
            return self.access_token
        else:
            return None

    def get_playback_token(self):
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}"
        }

        response = requests.get("https://api.spotify.com/v1/me/player", headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data["device"]["id"], data["timestamp"], data["progress_ms"], data["item"]["uri"]
        else:
            return None

    def refresh_token(self):
        headers = {
            "Authorization": f"Basic {base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}"
        }

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            self.token_type = data["token_type"]
            self.token_expiration_time = datetime.now() + timedelta(seconds=data["expires_in"])
            return self.access_token
        else:
            return None

    def call(self, method, endpoint, params=None, data=None, json=None, headers=None):
        headers = headers or {}
        headers["Authorization"] = f"Bearer {self.get_access_token()}"
        headers["Content-Type"] = "application/json"
        
        response = requests.request(method, endpoint, params=params, data=data, json=json, headers=headers)
        return response.json()