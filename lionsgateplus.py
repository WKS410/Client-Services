import requests

class StarzClient:
    def __init__(self):
        self.base_url = 'https://auth.starz.com/'
        self.auth_url = 'https://auth.starz.com/api/v4/User/login'
        self.auth_token = None
        
        self.headers = {
            'authority': 'auth.starz.com',
            'accept': '*/*',
            'accept-language': 'es-ES,es;q=0.9',
            'access-control-request-headers': 'authtokenauthorization,content-type',
            'access-control-request-method': 'POST',
            'origin': 'https://www.lionsgateplus.com',
            'referer': 'https://www.lionsgateplus.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        }

    def login(self, email, password):
        json_data = {
            'code': 'QH94',
            'emailAddress': email,
            'password': password,
        }
        
        # Make an OPTIONS request to the auth URL to retrieve the auth token
        options_response = requests.options(self.auth_url, headers=self.headers)
        self.auth_token = options_response.headers['authtokenauthorization']
        
        # Add the auth token to the headers and make a POST request to login
        self.headers['authtokenauthorization'] = self.auth_token
        response = requests.post(self.auth_url, headers=self.headers, json=json_data)
        
        # Check if the login was successful
        if response.status_code == 200 and response.json().get('success'):
            print('Login successful!')
        else:
            print('Login failed. Please check your email and password.')

    def get_movie(self, movie_id):
        url = f"{self.base_url}/movies/{movie_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_movies(self, params=None):
        url = f"{self.base_url}/movies"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_show(self, show_id):
        url = f"{self.base_url}/shows/{show_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_shows(self, params=None):
        url = f"{self.base_url}/shows"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_season(self, season_id):
        url = f"{self.base_url}/seasons/{season_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_seasons(self, params=None):
        url = f"{self.base_url}/seasons"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_episode(self, episode_id):
        url = f"{self.base_url}/episodes/{episode_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_episodes(self, params=None):
        url = f"{self.base_url}/episodes"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_video_manifest(self, video_id):
        url = f"{self.base_url}/videos/{video_id}/manifest"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        manifest = response.json()
        print(manifest)
        return manifest