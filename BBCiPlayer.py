import os
import sys
import requests

DEFAULTS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

class BBCiPlayerClient:
    def __init__(self, settings=None, **kwargs):
        if settings:
            DEFAULTS.update(settings)
        self.session = requests.session()
        self.session.headers.update({"user-agent": DEFAULTS["user-agent"]})
        self.session.proxies = kwargs.get("proxy", None)

    def get_metadata(self, pid: str, series_id: str) -> dict:
        query = {
            "id": "5692d93d5aac8d796a0305e895e61551",
            "variables": {
                "id": pid,
                "page": 1,
                "perPage": 100,
                "sliceId": series_id
            }
        }
        r = self.session.post(
            url="https://graph.ibl.api.bbc.co.uk/",
            headers={"Content-Type": "application/json"},
            json=query,
        ).json()["data"]["programme"]
        if r["entities"]["pagination"]["perPage"] < r["entities"]["pagination"]["count"]:
            query["variables"]["page"] = 2
            s = self.session.post(
                url="https://graph.ibl.api.bbc.co.uk/",
                headers={"Content-Type": "application/json"},
                json=query,
            ).json()["data"]["programme"]
            r["entities"]["results"].extend(s["entities"]["results"])
        return r


    def get_media(self, media_id: str, path: str, codec: str) -> dict:
        playlist = self.session.get(f"https://www.bbc.co.uk/programmes/{media_id}/playlist.json").json()
        vpid=playlist["defaultAvailableVersion"]["smpConfig"]["items"][0]["vpid"]
        mediaset = 'iptv-uhd' if codec == 'h265' else "iptv-all"
        old_ciphers = requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "DEFAULT:@SECLEVEL=1"
        r = self.session.get(f"https://securegate.iplayer.bbc.co.uk/mediaselector/6/select/version/2.0/vpid/{vpid}/format/json/mediaset/{mediaset}/proto/https",
                             cert=os.path.join(path, "bbciplayer_cert.pem")).json()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = old_ciphers
        if not 'media' in r:
            print('Video codec not available')
            sys.exit(1)
        for c in [x for x in r['media'] if x['kind'] == 'video']:
            connections = sorted(c["connection"], key=lambda x: x["priority"])
            if codec == "h265":
                for x in connections:
                    if not "akamai" in x["supplier"]:
                        connection = x
                        break
            else:
                connection = next(
                    x for x in connections
                    if x["supplier"] == "mf_cloudfront" and x["transferFormat"] == "hls"
                )
            break
        for c in [x for x in r['media'] if x['kind'] == 'captions']:
            connections = sorted(c["connection"], key=lambda x: x["priority"])
            subs = [x for x in connections if x["supplier"] == "mf_cloudfront"]
        manifest_url = connection['href']
        subs = {'url':subs[0]['href']}
        if codec == 'h264':
            manifest_url = '/'.join(connection["href"].replace(".hlsv2.ism", "").split("?")[0].split("/")[0:-1] + ["hls", "master.m3u8"])
            old_ciphers = requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "DEFAULT:@SECLEVEL=1"
            r = self.session.get(f"https://securegate.iplayer.bbc.co.uk/mediaselector/6/select/version/2.0/vpid/{vpid}/format/json/mediaset/iptv-uhd/proto/https", "YOUR CERT").json()
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = old_ciphers
            if not 'media' in r:
                return manifest_url, manifest_url, [subs]
            else:
                for c in [x for x in r['media'] if x['kind'] == 'video']:
                    connections = sorted(c["connection"], key=lambda x: x["priority"])
                    for x in connections:
                        if not "akamai" in x["supplier"]:
                            connection = x
                            break
                manifest_audio_url = connection['href']
                return manifest_url, manifest_audio_url, [subs]

        return manifest_url, manifest_url, [subs]