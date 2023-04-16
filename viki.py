import requests

class VikiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.viki.io/v4"
        self.session = requests.Session()
        self.headers = {
            'authority': 'www.viki.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.viki.com',
            'referer': 'https://www.viki.com/',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        }

    def _make_request(self, endpoint, params=None, method="get", json_data=None):
        url = f"{self.base_url}/{endpoint}.json?app=100000a&t={self.api_key}"
        if method == "get":
            response = self.session.get(url, params=params)
        else:
            response = self.session.post(url, json=json_data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_subtitles(self, video_id, language='en'):
        endpoint = f"{self.base_url}/videos/{video_id}/subtitles.json?language={language}&t={self.api_key}"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()

    def login(self, username, password, captcha_response):
        endpoint = "users/sign-in"
        headers = {"Referer": "https://www.viki.com/"}
        json_data = {"username": username, "password": password, "gRecaptchaResponse": captcha_response, "language": "en"}
        response = self._make_request(endpoint, method="post", json_data=json_data, headers=headers)
        if response is not None and "token" in response:
            token = response["token"]
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            return True
        else:
            return False

    def get_video_info(self, video_id):
        endpoint = f"videos/{video_id}"
        return self._make_request(endpoint)

    def search_videos(self, query, page=1):
        endpoint = "search"
        params = {"q": query, "per_page": 10, "page": page}
        return self._make_request(endpoint, params=params)
