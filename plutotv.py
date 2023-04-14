from uuid import uuid4
from datetime import datetime
import requests
from requests import Response


DEFAULTS = {
    "app": "web",
    "appVersion": "5.104.0-fc05a40ec3398e1c458e588d8a4e6a16e57579a5",
    "deviceVersion": "94.0.4606",
    "deviceModel": "web",
    "deviceMake": "chrome",
    "deviceType": "web",
    "clientId": uuid4(),
    "clientModelNumber": "1.0.0",
    "serverSideAds": False,
    "headers": {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    },
}


class PlutotvClient:
    def __init__(self, config=None, **kwargs):
        if config is None:
            config = {}

        self.config = DEFAULTS.copy()
        self.config.update(config)

        self.session = requests.session()
        self.session.headers.update(self.config["headers"])
        self.session.proxies = kwargs.get("proxies")

        self.app = self.config["app"]
        self.app_version = self.config["appVersion"]
        self.device_version = self.config["deviceVersion"]
        self.device_model = self.config["deviceModel"]
        self.device_make = self.config["deviceMake"]
        self.device_type = self.config["deviceType"]
        self.client_id = self.config["clientId"]
        self.client_model_number = self.config["clientModelNumber"]
        self.server_side_ads = self.config["serverSideAds"]

        self.media_url = None

    def start_session(self, slug: str) -> dict:
        client_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        r = self.session.get("https://boot.pluto.tv/v4/start",
                             params={
                                 "appName": self.app,
                                 "appVersion": self.app_version,
                                 "deviceVersion": self.device_version,
                                 "deviceModel": self.device_model,
                                 "deviceMake": self.device_make,
                                 "deviceType": self.device_type,
                                 "clientID": self.client_id,
                                 "clientModelNumber": self.client_model_number,
                                 "episodeSlugs": slug,
                                 "serverSideAds": self.server_side_ads,
                                 "constraints": "",
                                 "clientTime": client_time,
                             }).json()
        self.session.headers.update({"authorization": r["sessionToken"]})
        return r

    def get_metadata(self, slug: str) -> dict:
        r = self.start_session(slug)
        self.media_url = f"https://service-stitcher-ipv4.clusters.pluto.tv/v2{r['VOD'][0]['stitched']['path']}?{r['stitcherParams']}"
        return r

    def get_metadata_android(self, slug: str) -> dict:
        r = self.start_session(slug)
        self.media_url = f"https://api.pluto.tv/v2/episodes/{r['VOD'][0]['id']}/clips.json"
        return r

    def get_media(self) -> Response:
        return self.session.get(self.media_url)

    def search_channels(self, query: str) -> dict:
        r = self.session.get("https://service-gateway.pluto.tv/v3/channels/search", params={"query": query}).json()