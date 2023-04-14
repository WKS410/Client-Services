import json
import requests

class YouTubeClient:
    """
    Cliente para la API de YouTube
    """

    BASE_URL = 'https://www.googleapis.com/youtube/v3'

    def __init__(self, api_key):
        """
        Inicializa el cliente
        """
        self.api_key = api_key

    def _request(self, method, endpoint, data=None, params=None):
        """
        Realiza una solicitud HTTP a la API
        """
        url = self.BASE_URL + endpoint
        if not params:
            params = {}
        params['key'] = self.api_key
        response = requests.request(method, url, data=data, params=params)
        return response

    # Recursos de la API

    def get_video_info(self, video_id):
        """
        Obtiene información detallada de un video por su ID
        """
        endpoint = '/videos'
        params = {
            'part': 'snippet,contentDetails,statistics',
            'id': video_id
        }
        response = self._request('GET', endpoint, params=params)
        return response.json()

    def get_channel_info(self, channel_id):
        """
        Obtiene información detallada de un canal por su ID
        """
        endpoint = '/channels'
        params = {
            'part': 'snippet,statistics',
            'id': channel_id
        }
        response = self._request('GET', endpoint, params=params)
        return response.json()

    def get_playlist_info(self, playlist_id):
        """
        Obtiene información detallada de una lista de reproducción por su ID
        """
        endpoint = '/playlists'
        params = {
            'part': 'snippet',
            'id': playlist_id
        }
        response = self._request('GET', endpoint, params=params)
        return response.json()

    def get_video_comments(self, video_id, max_results=20):
        """
        Obtiene los comentarios de un video por su ID
        """
        endpoint = '/commentThreads'
        params = {
            'part': 'snippet',
            'videoId': video_id,
            'maxResults': max_results
        }
        response = self._request('GET', endpoint, params=params)
        return response.json()

    def get_channel_videos(self, channel_id, max_results=20):
        """
        Obtiene los videos de un canal por su ID
        """
        endpoint = '/search'
        params = {
            'part': 'snippet',
            'channelId': channel_id,
            'type': 'video',
            'maxResults': max_results
        }
        response = self._request('GET', endpoint, params=params)
        return response.json()

    def get_playlist_videos(self, playlist_id, max_results=20):
        """
        Obtiene los videos de una lista de reproducción por su ID
        """
        endpoint = '/playlistItems'
        params = {
            'part': 'snippet',
            'playlistId': playlist_id,
            'maxResults': max_results
        }
        response = self._request('GET', endpoint, params=params)
        return response.json()
