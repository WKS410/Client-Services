from enum import Enum
import base64
import requests


class Client:
    def __init__(self, config=None, **kwargs):
        DEFAULT_HEADERS = {
            'user-agent': 'com.apple.tv/1.0 iOS/13.4.5 AppleTV/13.4.5 model/AppleTV6,2 hwp/t8011 build/17L562 (3; dt:163)',
        }
        
        if config is None:
            config = {}

        self.config = {
            **{'headers': DEFAULT_HEADERS},
            **config
        }

        self.session = requests.Session()
        self.session.headers.update(self.config["headers"])

    def login(self, username: str, password: str) -> dict:
        """
        Here you add the code to log into the SERVICE
        :param username: Username/E-Mail of the account
        :param password: Password of the account
        :return:
        """
        r = self.session.post(
            "https://setup.icloud.com/setup/ws/1/login?clientBuildNumber=2110Project46&clientId=d13dd300-b146-47bf-9bdd-ac9a0048ccfe",
            headers={"origin": "https://www.icloud.com"},
            json={
                "apple_id": username,
                "password": password,
                "extended_login": False  # todo what does that mean, do I always have to log in again?
            }
        ).json()
        
        if "dsInfo" not in r:
            raise RuntimeError("Login Failed")
            
        self.session.headers.update({"x-dsid": r["dsInfo"]["dsid"]})
        return r

    def get_series(self, series_id: str) -> dict:
        """
        Here you add the code to get metadata of a series
        :param series_id:
        :return: metadata of the series
        """

    def get_movie(self, movie_id: str) -> dict:
        """
        Here you add the code to get metadata for a movie
        :param movie_id: id of the movie
        :return: metadata of the movie
        """

    def get_season(self, season: str) -> dict:
        """
        Here you add the code to get a specific season
        :param season: can be a number or a season id
        :return: metadata of the season
        """

    def get_metadata(self, content_id: str) -> dict:
        """
        Get metadata of a video by a content id
        :param content_id: id of the video
        :return: metadata of the video
        """
        r = self.session.get(
            content_id,
            headers={
                "authority": "itunes.apple.com",
                "accept": "application/vnd.api+json",
                # "user-agent": "ATVE/6.2.0 Android/10 build/6A226 maker/Google model/Chromecast FW/QTS2.200918.0337115981"
            },
            params={
                "isWebExpV2": True,
                "dataOnly": True
            }
        ).json()
        return r

    def get_rental_id(self):
        r = self.session.get(
            "https://uts-api.itunes.apple.com/uts/v3/shelves/uts.col.UpNext?caller=js&locale=en-US&pfm=web&sf=143441&utscf=OjAAAAEAAAAAAAIAEAAAAAwADQAQAA~~&utsk=f1f4d4b23f8188ac::::::88f7d2e604b15077&v=56").json()

        return r

class ResponseCode(Enum):
    OK = 0
    INVALID_PSSH = -1001
    NOT_OWNED = -1002  # Title not owned in the requested quality
    TOO_MANY_DEVICES = -1004
    INSUFFICIENT_SECURITY = -1021  # L1 required or the key used is revoked


class ITunesException(Exception):
    class LoginError(Exception):
        """Error during login"""

    class WidevineError(Exception):
        """Error during license"""
