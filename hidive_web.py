import json
import requests

class HIDIVEWebClient:
    """
    Cliente para la API web de HIDIVE
    """

    BASE_URL = 'https://www.hidive.com'

    def __init__(self):
        """
        Inicializa el cliente
        """
        self.session = requests.Session()

    def _request(self, method, endpoint, data=None, params=None):
        """
        Realiza una solicitud HTTP a la API web
        """
        url = self.BASE_URL + endpoint
        response = self.session.request(method, url, data=data, params=params)
        return response

    # Recursos de la API web

    def search(self, query):
        """
        Busca anime por nombre
        """
        endpoint = '/search?q=' + query
        response = self._request('GET', endpoint)
        return response.content

    def get_anime(self, slug):
        """
        Obtiene información detallada de un anime por su slug
        """
        endpoint = '/anime/' + slug
        response = self._request('GET', endpoint)
        return response.content

    def get_video_sources(self, slug, episode_num):
        """
        Obtiene las fuentes de video disponibles de un episodio de un anime por su slug y número de episodio
        """
        endpoint = f'/anime/{slug}/episode/{episode_num}'
        response = self._request('GET', endpoint)
        sources = {}
        if response.status_code == 200:
            data = response.content.decode('utf-8')
            start_index = data.find('window.__INITIAL_STATE__')
            if start_index != -1:
                start_index += len('window.__INITIAL_STATE__ = ')
                end_index = data.find(';</script>', start_index)
                if end_index != -1:
                    json_data = data[start_index:end_index]
                    initial_state = json.loads(json_data)
                    streams = initial_state.get('playback', {}).get('streams', [])
                    for stream in streams:
                        if 'url' in stream and 'format' in stream:
                            sources[stream['format']] = stream['url']
        return sources

    def login(self, username, password):
        """
        Inicia sesión en HIDIVE con el nombre de usuario y la contraseña proporcionados
        """
        endpoint = '/account/login'
        response = self._request('GET', endpoint)
        data = {
            'username': username,
            'password': password,
            'submit': 'Login'
        }
        start_index = response.content.find('name="__RequestVerificationToken"')
        if start_index != -1:
            start_index = response.content.find('value="', start_index) + len('value="')
            end_index = response.content.find('"', start_index)
            if end_index != -1:
                data['__RequestVerificationToken'] = response.content[start_index:end_index]
        response = self._request('POST', endpoint, data=data)
        return response
