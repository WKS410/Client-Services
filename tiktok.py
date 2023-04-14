import requests


class TikTokClient:
    def __init__(self, session=None):
        self.base_url = "https://api.tiktok.com"
        self.session = session or requests.Session()
    
    def search_users(self, keyword):
        endpoint = f"{self.base_url}/discover/search/"
        params = {
            "type": "1",
            "count": "30",
            "keyword": keyword
        }
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_user_info(self, user_id):
        endpoint = f"{self.base_url}/user/detail/"
        params = {
            "unique_id": user_id
        }
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_user_videos(self, user_id, count=30):
        endpoint = f"{self.base_url}/video/feed/"
        params = {
            "count": count,
            "minCursor": 0,
            "maxCursor": 0,
            "user_id": user_id,
            "aid": "1988"
        }
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_hashtag_videos(self, hashtag, count=30):
        endpoint = f"{self.base_url}/video/feed/"
        params = {
            "count": count,
            "minCursor": 0,
            "maxCursor": 0,
            "hashtag": hashtag,
            "aid": "1988"
        }
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def login(self, username, password):
        endpoint = f"{self.base_url}/passport/user/login/"
        data = {
            "username": username,
            "password": password,
            "email": "",
            "phone_number": "",
            "user_region": "",
            "referer": "",
            "is_page_url": False,
            "login_type": 4,
            "device_id": self.device_id,
            "from": "tiktok_pc",
            "_csrf": csrf_token,
        }
        response = self.session.post(
            "https://www.tiktok.com/login/",
            data=data,
            allow_redirects=False,
        )

        # Check if login was successful by checking the response status code and URL
        if response.status_code == 302 and response.headers.get("Location") == "https://www.tiktok.com/":
            return True

        return False