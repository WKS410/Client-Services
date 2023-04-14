import json
import requests

class HIDIVEClient:
    """
    Cliente para la API de HIDIVE
    """

    BASE_URL = 'https://api.hidive.com/v1'

    def __init__(self, client_id, client_secret):
        """
        Inicializa el cliente
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires = None

    def _request(self, method, endpoint, data=None, params=None):
        """
        Realiza una solicitud HTTP a la API
        """
        headers = {}
        if self.access_token:
            headers['Authorization'] = 'Bearer ' + self.access_token
        url = self.BASE_URL + endpoint
        response = requests.request(method, url, headers=headers, data=data, params=params)
        if response.status_code == 401:
            self._refresh_token()
            headers['Authorization'] = 'Bearer ' + self.access_token
            response = requests.request(method, url, headers=headers, data=data, params=params)
        return response

    def _refresh_token(self):
        """
        Refresca el token de acceso
        """
        endpoint = '/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.BASE_URL + endpoint, data=data)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('access_token')
            self.token_expires = data.get('expires_in')

    # Recursos de la API

    def get_anime(self, anime_id):
        """
        Obtiene información detallada de un anime por su ID
        """
        endpoint = f'/anime/{anime_id}'
        response = self._request('GET', endpoint)
        return response.json()

    def get_episode(self, episode_id):
        """
        Obtiene información detallada de un episodio por su ID
        """
        endpoint = f'/episodes/{episode_id}'
        response = self._request('GET', endpoint)
        return response.json()

    def get_season(self, season_id):
        """
        Obtiene información detallada de una temporada por su ID
        """
        endpoint = f'/seasons/{season_id}'
        response = self._request('GET', endpoint)
        return response.json()

    def get_stream_url(self, stream_id):
        """
        Obtiene la URL del flujo de video por su ID
        """
        endpoint = f'/stream/{stream_id}'
        response = self._request('GET', endpoint)
        return response.json()
