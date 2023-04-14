import requests

class AnimeOnegaiClient:
    """
    Cliente para la API de AnimeOnegai
    """

    BASE_URL = 'https://animeonegai.com/api/v1/'

    def __init__(self, api_key=None, secret_key=None):
        """
        Inicializa el cliente con claves API y secretas (opcional)
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.token = None

    def _get_token(self):
        """
        Genera un token de autenticación utilizando las claves API y secretas
        """
        url = self.BASE_URL + 'authenticate'
        data = {
            'apiKey': self.api_key,
            'secretKey': self.secret_key
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.token = response.json()['token']
        else:
            print('Error al generar token:', response.json()['message'])

    def _request(self, method, endpoint, data=None, params=None):
        """
        Realiza una solicitud HTTP a la API con el token de autenticación (si es necesario)
        """
        url = self.BASE_URL + endpoint
        headers = {}
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token
        response = requests.request(method, url, json=data, params=params, headers=headers)
        if response.status_code == 401 and self.api_key and self.secret_key:
            self._get_token()
            headers['Authorization'] = 'Bearer ' + self.token
            response = requests.request(method, url, json=data, params=params, headers=headers)
        return response.json()

    # Recursos de la API

    def search_anime(self, query):
        """
        Busca anime por nombre
        """
        endpoint = 'anime'
        params = {'search': query}
        return self._request('GET', endpoint, params=params)

    def get_anime(self, anime_id):
        """
        Obtiene información detallada de un anime por su ID
        """
        endpoint = f'anime/{anime_id}'
        return self._request('GET', endpoint)

    def get_anime_episodes(self, anime_id):
        """
        Obtiene los episodios de un anime por su ID
        """
        endpoint = f'anime/{anime_id}/episodes'
        return self._request('GET', endpoint)

    def get_anime_comments(self, anime_id):
        """
        Obtiene los comentarios de un anime por su ID
        """
        endpoint = f'anime/{anime_id}/comments'
        return self._request('GET', endpoint)

    def get_manga(self, manga_id):
        """
        Obtiene información detallada de un manga por su ID
        """
        endpoint = f'manga/{manga_id}'
        return self._request('GET', endpoint)

    def get_manga_chapters(self, manga_id):
        """
        Obtiene los capítulos de un manga por su ID
        """
        endpoint = f'manga/{manga_id}/chapters'
        return self._request('GET', endpoint)

    def get_manga_comments(self, manga_id):
        """
        Obtiene los comentarios de un manga por su ID
        """
        endpoint = f
