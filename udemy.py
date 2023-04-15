import requests
import json


class UdemyAPI:
    def __init__(self, client_id, client_secret, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.access_token = None
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        }
        self.token_url = "https://www.udemy.com/api-2.0/oauth/token/"

    def _get_access_token(self):
        """
        Obtiene el token de acceso a la API utilizando las credenciales de usuario.
        """
        token_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "scope": "basic",
        }
        response = requests.post(self.token_url, data=token_data)
        if response.ok:
            self.access_token = json.loads(response.content)["access_token"]
            self.headers["Authorization"] = f"Bearer {self.access_token}"
            return True
        else:
            return False

    def get_course_info(self, course_id):
        """
        Obtiene información sobre un curso.
        """
        if not self.access_token:
            self._get_access_token()

        course_url = f"https://www.udemy.com/api-2.0/courses/{course_id}/"
        response = requests.get(course_url, headers=self.headers)
        if response.ok:
            course_data = json.loads(response.content)
            return course_data
        else:
            return {}

    def get_courses(self, page=1, page_size=50):
        """
        Obtiene la lista de cursos del usuario.
        """
        if not self.access_token:
            self._get_access_token()

        courses_url = f"https://www.udemy.com/api-2.0/users/me/subscribed-courses/?page={page}&page_size={page_size}"
        response = requests.get(courses_url, headers=self.headers)
        if response.ok:
            courses_data = json.loads(response.content)["results"]
            return courses_data
        else:
            return []

    def get_course_progress(self, course_id):
        """
        Obtiene el progreso de un curso.
        """
        if not self.access_token:
            self._get_access_token()

        progress_url = f"https://www.udemy.com/api-2.0/users/me/courses/{course_id}/progress/"
        response = requests.get(progress_url, headers=self.headers)
        if response.ok:
            progress_data = json.loads(response.content)
            return progress_data
        else:
            return {}