import requests
import webbrowser
from urllib.parse import urlparse, parse_qs
import json

class GithubClient:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.authenticated = False
        self.base_url = 'https://api.github.com'

    def authenticate(self):
        auth_url = f'https://github.com/login/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=repo'
        webbrowser.open(auth_url)
        print('Please authorize the application to access your GitHub account.')
        redirect_url = input('Enter the URL you were redirected to: ')
        parsed_url = urlparse(redirect_url)
        auth_code = parse_qs(parsed_url.query)['code'][0]
        headers = {
            'Accept': 'application/json'
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }
        response = requests.post('https://github.com/login/oauth/access_token', headers=headers, data=data)
        response_data = json.loads(response.content.decode('utf-8'))
        self.access_token = response_data['access_token']
        self.authenticated = True
        print('Authentication successful.')

    def make_request(self, method, endpoint, data=None):
        headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if self.authenticated:
            headers['Authorization'] = f'Bearer {self.access_token}'
        url = f'{self.base_url}/{endpoint}'
        response = requests.request(method, url, headers=headers, json=data)
        response_data = json.loads(response.content.decode('utf-8'))
        return response_data

    def list_repositories(self):
        return self._make_request("GET", "/user/repos")

    def create_repository(self, name, private=False, description=None):
        data = {
            "name": name,
            "private": private,
            "description": description
        }
        return self._make_request("POST", "/user/repos", data=data)    
    
    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }