import hashlib
import urllib.parse
import datetime

class RakuTVClient:
    def __init__(self, title, vquality, achannels, market, locale):
        self.title = title
        self.vquality = vquality
        self.achannels = achannels
        self.market = market
        self.locale = locale

        self.range = None
        self.app_version = "3.7.3b"
        self.classification_id = 41
        self.device_identifier = "android"
        self.device_serial = "6cc3584a-c182-4cc1-9f8d-b90e4ed76de9"
        self.access_token = None
        self.session_uuid = None
        self.player = "andtv:DASH-CENC:WVM"
        self.license_url = None

        self.session = None

    def configure(self, session):
        self.session = session

    def login_android(self, username, password):
        login_url = "https://gizmo.rakuten.tv/v3/me/login?" + urllib.parse.urlencode({
            "device_identifier": self.device_identifier,
            "device_serial": self.device_serial,
            "locale": self.locale,
            "market_code": self.market,
            "timestamp": f"{int(datetime.datetime.now().timestamp())}010"
        })
        login_url += "signature=" + self.generate_signature(login_url)
        login = self.session.post(
            url=login_url,
            data={
                "password": password,
                "username": username,
            },
        ).json()
        if "errors" in login:
            error = login["errors"][0]
            raise ValueError(f"Unable to login: {error['message']} [{error['code']}]")
        self.access_token = login["data"]["access_token"]
        self.session_uuid = login["data"]["session_uuid"]

    def generate_signature(self, url):
        return hashlib.md5((url + self.access_token).encode()).hexdigest()

    def get_titles(self):
        title_url = f"https://gizmo.rakuten.tv/v3/movies/{self.title}?" + urllib.parse.urlencode({
            "classification_id": self.classification_id,
            "device_identifier": self.device_identifier,
            "device_serial": self.device_serial,
            "locale": self.locale,
            "market_code": self.market,
            "session_uuid": self.session_uuid,
            "timestamp": f"{int(datetime.datetime.now().timestamp())}005"
        })
        title_url += "signature=" + self.generate_signature(title_url)
        title = self.session.get(url=title_url).json()
        if "errors" in title:
            error = title["errors"][0]
            if error["code"] == "error.not_found":
                raise ValueError(f"Title [{self.title}] was not found on this account.")
            else:
                raise ValueError(f"Unable to get title info: {error['message']} [{error['code']}]")
        title = title["data"]
        return title

def get_tracks(self, title):
    stream_info_url = "https://gizmo.rakuten.tv/v3/me/streamings?" + urllib.parse.urlencode({
        "device_stream_video_quality": self.vquality,
        "device_identifier": self.device_identifier,
        "market_code": self.market,
        "session_uuid": self.session_uuid,
        "timestamp": f"{int(datetime.datetime.now().timestamp())}122"
    })
    stream_info_url += "signature=" + self.generate_signature(stream_info_url)
    stream_info = self.session.post(
        url=stream_info_url,
        data={
            "hdr_type": {"SDR": "NONE", "HDR10": "HDR10", "DV": "DOLBY_VISION"}.get(self.range),
            "audio_quality": self.achannels,
            "app_version": self.app_version,
            "content_id": self.title,
            "video_quality": self.vquality,
            "audio_language": "ENG",
            "video_type": "stream",
            "device_serial": self.device_serial,
            "content_type": "movies" if self.movie else "episodes",
            "classification_id": self.classification_id,
            "subtitle_language": "MIS",
            "player": self.player
        }
    ).json()
    if "errors" in stream_info:
        error = stream_info["errors"][0]
        raise self.log.exit(f" - Failed to get track info: {error['message']} [{error['code']}]")
    stream_info = stream_info["data"]["stream_infos"][0]

    self.license_url = stream_info["license_url"]

    tracks = Tracks.from_mpd(
        url=stream_info["url"],
        session=self.session,
        source=self.ALIASES[0]
    )

    for sub in stream_info.get("all_subtitles") or []:
        if sub["type"] in ["Subtitles-Burned"]:
            continue
        tracks.add(TextTrack(
            id_=hashlib.md5(sub["url"].encode()).hexdigest()[0:6],
            source=self.ALIASES[0],
            url=sub["url"],
            codec="srt",
            language=sub["locale"],
        ))
    
    return tracks
