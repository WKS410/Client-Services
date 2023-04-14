import requests
from loguru import logger

from utils.tmdb import TMDB
from utils.widevine import Widevine


class ParaviJPClient:
    def __init__(self, session) -> None:
        self.domaine = "paravi.jp"

        self.endpoints = {
            "pathEvaluator": f"https://www.{self.domaine}/pathEvaluator",
            "metas": f"https://api.{self.domaine}/api/v1/metas/",
        }

        self.session = session

        self.tmdb = TMDB(self.session)

    def get_tracks(self, watch_id):

        for i in range(1, 11):
            self.session.get("https://www.paravi.jp/api/user/token/refresh")

            reviews = self.session.get(
                "https://www.paravi.jp/api/profile/reviews",
                params={"meta_id": watch_id},
            ).json()

            if "authContext" in reviews:
                if "token" in reviews["authContext"] and "" in reviews["authContext"]:
                    token = reviews["authContext"]["token"]
                    uid = reviews["authContext"]["id"]

                    self.session.headers.update(
                        {"authorization": f"Bearer {token}", "x-user-id": str(uid)}
                    )

                    data = {
                        "meta_id": int(watch_id),
                        "vuid": "e70b67f100c115787882cd1d36a1b59c",
                        "device_code": 1,
                        "app_id": 1,
                        "user_id": uid,
                    }

                    playback = self.session.post(
                        "https://api.paravi.jp/api/v1/playback/auth", data=data
                    ).json()

                    if playback.get("error"):
                        logger.opt(colors=True).info(
                            f"<red>{playback['error']['message']}</red>"
                        )
                        continue

                    media_id = False
                    playback_session_id = False
                    if "media" in playback:
                        media_id = playback["media"]["ovp_video_id"]
                        playback_session_id = playback["playback_session_id"]
                    else:
                        logger.opt(colors=True).info(f"<red>No media in playback</red>")
                        continue

                    if media_id and playback_session_id:
                        self.session.headers.update(
                            {"x-playback-session-id": playback_session_id}
                        )

                        media = self.session.get(
                            f"https://playback.paravi.jp/session/open/v1/merchants/paravi/medias/{media_id}",
                            params={"user_id": uid},
                        ).json()

                        widevine = Widevine(self.session, media)
                        tracks = widevine.get_tracks()

                        return tracks

        return []
