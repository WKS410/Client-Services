import requests
import json

class KOCOWAClient:
    def __init__(self, email, password):
        self.BASE_URL = 'https://api.kocowa.com/v1'
        self.email = email
        self.password = password
        self.access_token = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/json',
        }

    def login(self):
        login_url = f"{self.BASE_URL}/auth/login"
        data = {
            "email": self.email,
            "password": self.password
        }
        response = requests.post(login_url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            self.headers['Authorization'] = f"Bearer {self.access_token}"
            return True
        else:
            return False

    def get_dramas(self):
        dramas_url = f"{self.BASE_URL}/contents/dramas"
        response = requests.get(dramas_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return []

    def get_drama(self, drama_id):
        drama_url = f"{self.BASE_URL}/contents/dramas/{drama_id}"
        response = requests.get(drama_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return {}

    def get_episode(self, episode_id):
        episode_url = f"{self.BASE_URL}/contents/episodes/{episode_id}"
        response = requests.get(episode_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return {}

    def search(self, query):
        search_url = f"{self.BASE_URL}/search"
        params = {
            "query": query
        }
        response = requests.get(search_url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return []

    def get_my_list(self):
        my_list_url = f"{self.BASE_URL}/my/list"
        response = requests.get(my_list_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return []

    def add_to_my_list(self, content_id):
        add_url = f"{self.BASE_URL}/my/list"
        data = {
            "content_id": content_id
        }
        response = requests.post(add_url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            return True
        else:
            return False

    def remove_from_my_list(self, content_id):
        remove_url = f"{self.BASE_URL}/my/list/{content_id}"
        response = requests.delete(remove_url, headers=self.headers)
        if response.status_code == 200:
            return True
        else:
            return False
