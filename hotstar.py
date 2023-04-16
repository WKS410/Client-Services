import hmac
import json
import time
from hashlib import sha256

import requests


class HotstarClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.device_id = self.__get_device_id()
        self.authtoken = None
        self.user_id = None
        self.config = {
            "version": "10.8.5",
            "platform": "web",
            "os": "Windows",
            "User-Agent": "Hotstar/7.15.1 (iPhone; iOS 13.3; Scale/2.00)",
            "osVersion": "10",
            "deviceId": self.device_id,
        }

    def __get_device_id(self):
        return "WEB|" + sha256(str(time.time()).encode()).hexdigest()[:16]

    def __generate_auth(self):
        AKAMAI_ENCRYPTION_KEY = b'\x05\xfc\x1a\x01\xca\xc9\x4b\xc4\x12\xfc\x53\x12\x07\x75\xf9\xee'
        st = int(time.time())
        exp = st + 6000
        hotstarauth = f'st={st}~exp={exp}~acl=/*'
        hotstarauth += '~hmac=' + hmac.new(AKAMAI_ENCRYPTION_KEY, hotstarauth.encode(), sha256).hexdigest()
        return hotstarauth

    def login(self):
        login_url = "https://api.hotstar.com/in/aadhar/v2/web/in/user/login"
        data = {"username": self.username, "password": self.password}
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Hotstar/7.15.1 (iPhone; iOS 13.3; Scale/2.00)",
            "hotstarauth": self.__generate_auth(),
            "X-HS-Platform": self.config["platform"],
            "X-HS-AppVersion": self.config["version"],
            "X-HS-UserAgent": "hotstar-web-app/10.8.5 Chrome/88.0.4324.182 Windows",
            "X-HS-DeviceInfo": json.dumps(
                {
                    "build_version": self.config["version"],
                    "device": self.config["os"],
                    "device_manufacturer": "",
                    "device_model": "",
                    "os_version": self.config["osVersion"],
                }
            ),
        }
        response = requests.post(login_url, json=data, headers=headers).json()
        if response.get("statusCode") == 200:
            self.authtoken = response["body"]["token"]
            self.user_id = response["body"]["userId"]
            return True
        else:
            return False

    def __refresh_token(self):
        refresh_url = f"https://api.hotstar.com/in/aadhar/v2/web/in/user/refresh-token?userId={self.user_id}"
        headers = {
            "hotstarauth": self.__generate_auth(),
            "X-HS-UserToken": self.authtoken,
            "User-Agent": "Hotstar/7.15.1 (iPhone; iOS 13.3; Scale/2.00)",
            "X-HS-Platform": self.config["platform"],
            "X-HS-AppVersion": self.config["version"],
        }
        response = requests.get(refresh_url, headers=headers).json()
        if response.get("statusCode") == 200:
            self.authtoken = response["body"]["token"]

    def __get_bearer_token(self):
        url = "https://api.hotstar.com/in/aadhar/v2/web/in/user/login"
        headers = {
            "User-Agent": "Hotstar/7.15.1 (iPhone; iOS 13.3; Scale/2.00)",
            "X-HS-APPNAME": self.config["app_name"],
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "username": self.username,
            "password": self.password,
            "deviceId": self.device_id,
            "osName": "Windows",
            "osVersion": "10",
            "userData1": "",
            "userData2": "",
            "userData3": "",
            "userData4": "",
        }
        resp = self.session.post(url, headers=headers, data=data)
        if resp.status_code != 200:
            raise ValueError("Failed to get bearer token")
        return resp.json()["body"]["accessToken"]
    
    def get_manifest(self, content_id):
        if not self.access_token:
            self.login()

        manifest_url = f"https://api.hotstar.com/play/v1/play/content/{content_id}"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Hotstar/7.15.1 (iPhone; iOS 13.3; Scale/2.00)",
            "Authorization": f"Bearer {self.access_token}"
        }
        response = self.session.get(manifest_url, headers=headers)

        if response.status_code == 401:
            self.refresh_access_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = self.session.get(manifest_url, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.text)
            return data["body"]["media"]["stream"]
        else:
            print("Failed to get manifest.")
            return None
    