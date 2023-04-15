import requests
import hashlib
import time
import json

class BiliBiliClient:
    def __init__(self, app_key, app_secret):
        self.base_url = "https://api.bilibili.tv/"
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = None
        self.cookies = None

    # Función para realizar una solicitud a la API de Bilibili
    def call_api(self, endpoint, params={}):
        # Agregar los parámetros necesarios para la solicitud
        params["appkey"] = self.app_key
        params["ts"] = int(time.time())
        params["sign"] = self.generate_sign(params)

        # Realizar la solicitud
        response = requests.get(self.base_url + endpoint, params=params, cookies=self.cookies)

        # Interpretar la respuesta de la API como JSON
        data = json.loads(response.text)

        # Devolver los datos obtenidos
        return data

    # Función para generar la firma de la API de Bilibili
    def generate_sign(self, params):
        # Ordenar los parámetros alfabéticamente
        sorted_params = sorted(params.items(), key=lambda x: x[0])

        # Concatenar todos los valores de los parámetros en una sola cadena
        sign_str = ""
        for key, value in sorted_params:
            sign_str += f"{key}={value}"

        # Agregar la clave secreta a la cadena
        sign_str += self.app_secret

        # Calcular el valor MD5 de la cadena resultante
        md5 = hashlib.md5(sign_str.encode("utf-8")).hexdigest()

        # Devolver el valor MD5 como la firma de la API
        return md5

    # Función para iniciar sesión en Bilibili
    def login(self, username, password):
        # Realizar la solicitud de inicio de sesión
        endpoint = "https://passport.bilibili.tv/api/v2/oauth2/login"
        params = {
            "appkey": self.app_key,
            "username": username,
            "password": password,
            "ts": int(time.time())
        }
        response = requests.post(endpoint, data=params)

        # Interpretar la respuesta como JSON
        data = json.loads(response.text)

        # Verificar si se obtuvo un token de acceso
        if data["code"] != 0:
            raise Exception(f"No se pudo iniciar sesión: {data['message']}")

        # Guardar el token de acceso y las cookies necesarias para futuras solicitudes
        self.access_token = data["data"]["access_token"]
        self.cookies = response.cookies

    # Función para obtener la lista de videos de un usuario
    def get_user_videos(self, uid, page=1, pagesize=30):
        endpoint = "x/space/arc/search"
        params = {
            "mid": uid,
            "ps": pagesize,
            "tid": 0,
            "pn": page,
            "keyword": "",
            "order": "pubdate"
        }
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(self.base_url + endpoint, params=params, headers=headers, cookies=self.cookies)
        data = json.loads(response.text)
        return data

# Función para obtener información básica del usuario
def get_user_info(uid, access_token, cookies):
    endpoint = "x/space/acc/info"
    params = {"mid": uid}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(BASE_URL + endpoint, params=params, headers=headers, cookies=cookies)
    data = json.loads(response.text)
    return data
