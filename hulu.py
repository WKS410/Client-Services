import requests
from datetime import datetime

class HuluAPI:
    def __init__(self, client_id, client_secret, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None

    def _get_access_token(self):
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
        }

        data = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password
        }

        response = requests.post('https://auth.hulu.com/v1/token', headers=headers, data=data)

        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            self.refresh_token = response.json()['refresh_token']
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def _refresh_access_token(self):
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
        }

        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }

        response = requests.post('https://auth.hulu.com/v1/token', headers=headers, data=data)

        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            self.refresh_token = response.json()['refresh_token']
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def _make_request(self, method, url, params=None, headers=None, data=None):
        if not self.access_token:
            self._get_access_token()

        headers = headers or {}
        headers['authorization'] = f'Bearer {self.access_token}'

        response = requests.request(method, url, params=params, headers=headers, data=data)

        if response.status_code == 401:
            self._refresh_access_token()
            headers['authorization'] = f'Bearer {self.access_token}'
            response = requests.request(method, url, params=params, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def search(self, query):
        url = 'https://api.hulu.com/v1/search'
        params = {'query': query}
        return self._make_request('GET', url, params=params)

    def get_show_info(self, show_id):
        url = f'https://api.hulu.com/v1/shows/{show_id}'
        return self._make_request('GET', url)

    def get_episode_info(self, episode_id):
        url = f'https://api.hulu.com/v1/episodes/{episode_id}'
        return self._make_request('GET', url)

    def get_season_info(self, season_id):
        url = f'https://api.hulu.com/v1/seasons/{season_id}'
        return self._make_request('GET', url)

    def get_user_profile(self):
        url = 'https://api.hulu.com/v1/users/self/profile'
        return self._make_request('GET', url)

    def get_media(self, media_id: str) -> dict:
        payload = {
            'content_eab_id': media_id,
            'play_intent': 'resume',
            'unencrypted': True,
            'all_cdn': True,
            'ignore_kids_block': False,
            'device_identifier': self.provide_serial(),
            'deejay_device_id': self.config["device_id"],
            'version': 17,
            'include_t2_rev_beacon': False,
            'include_t2_adinteraction_beacon': False,
            'support_brightline': False,
            'support_innovid': False,
            'support_innovid_truex': False,
            'support_gateway': False,
            'limit_ad_tracking': True,
            'network_mode': 'Ethernet',
            'enable_selectors': False,
            'playback': {
                'version': 2,
                'video': {
                    'codecs': {
                        'values': [
                            {
                                'type': 'H264',
                                'width': 3840,
                                'height': 2160,
                                'framerate': 60,
                                'level': '4.2',
                                'profile': 'HIGH'
                            },
                            {
                                'type': 'H265',
                                'width': 3840,
                                'height': 2160,
                                'framerate': 60,
                                'level': '5.1',
                                'profile': 'MAIN_10',
                                'tier': 'MAIN'
                            }
                        ],
                        'selection_mode': 'ALL'
                    },
                    "dynamic_range": "HDR10PLUS",
                },
                'audio': {
                    'codecs': {
                        'values': [
                            {
                                'type': 'AAC'
                            },
                            {
                                'type': 'EC3'
                            }
                        ],
                        'selection_mode': 'ALL'
                    }
                },
                'drm': {
                    'values': [
                        {
                            'type': 'FAIRPLAY',
                        },
                        {
                            'type': 'WIDEVINE',
                            'version': 'MODULAR',
                            'security_level': 'L1'
                        },
                        {
                            "type": "PLAYREADY",
                            "version": "V2",
                            "security_level": "SL2000"
                        },
                    ],
                    'selection_mode': 'ALL',
                    'multi_key': True
                },
                'manifest': {
                    'type': 'DASH',
                    'https': True,
                    'multiple_cdns': False,
                    'patch_updates': True,
                    'hulu_types': False,
                    'live_dai': False,
                    'multiple_periods': False,
                    'xlink': False,
                    'secondary_audio': True,
                    'live_fragment_delay': 3
                },
                'segments': {
                    'values': [
                        {
                            "type": "MPEGTS",
                            "encryption": {
                                "mode": "CBCS",
                                "type": "SAMPLE_AES"
                            },
                            "muxed": True,
                            "https": True,
                        },
                        {
                            'type': 'FMP4',
                            'encryption': {
                                'mode': 'CENC',
                                'type': 'CENC'
                            },
                            'https': True
                        },
                        {
                            "type": "FMP4",
                            "encryption": {
                                "mode": "CBCS",
                                "type": "CENC"
                            },
                            "muxed": False,
                            "https": True,
                        }
                    ],
                    'selection_mode': 'ALL'
                }
            },
        }
        # todo update this
        payload.update({'lat': '0.0', 'long': '0.0'})

        r = self.session.post("https://play.hulu.com/v6/playlist",
                              headers={
                                  "Authorization": "Bearer " + self.access_token,
                              },
                              json=payload,
                              ).json()
        if "wv_server" not in r:
            print("wv_server variable missing (probably ip issue)")
            
    def get_live_tv_guide(self):
        url = "https://api.hulu.com/v1/live_tv/guide"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        params = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timezone": "America/New_York"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get live TV guide: {response.text}")