import requests
import time
import json
import base64

DEFAULTS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"
}


class VIXClient:
    def __init__(self, settings=None, **kwargs):
        if settings:
            DEFAULTS.update(settings)

        self.session = requests.session()
        self.license_url = None
        self.session.headers.update({"user-agent": DEFAULTS["user-agent"]})

    def get_series(self, series_id: str) -> dict:
        r = self.session.post(url='https://client-api.vix.com/gql/v1/',
        json={
            "operationName": "DetailData",
            "variables": {
                "id": "series:mcp:{0}".format(series_id),
                "navigationSection": {
                "urlPath": "/ondemand",
                "pageItemId": "d9ca04952cd5019288ee463471e7bf4bb0c693d2"
            },
            'pagination': {
                'first': None,
                'after': None,
                },
            },
            'query': 'query DetailData($id: ID!, $navigationSection: TrackingNavigationSectionInput!, $pagination: PaginationParams!) {\n  videoById(id: $id) {\n    detailPageMetadata {\n      ...PageMetadataFragment\n      __typename\n    }\n    vodAvailability {\n      isBlocked\n      reason\n      __typename\n    }\n    ...VideoContentFullFragment\n    videoTypeData {\n      ...VideoTypeMovieFullFragment\n      ... on VideoTypeExtraData {\n        ...VideoTypeExtraFullFragment\n        __typename\n      }\n      ... on VideoTypeSeriesData {\n        ...VideoTypeSeriesFullFragment\n        ...SeasonsConnectionFragment\n        __typename\n      }\n      ... on VideoTypeEpisodeData {\n        ...VideoTypeEpisodeFullFragment\n        series {\n          id\n          videoTypeData {\n            ... on VideoTypeSeriesData {\n              ...VideoTypeSeriesFullFragment\n              ...SeasonsConnectionFragment\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment VideoContentFullFragment on VideoContent {\n  ...VideoContentBasicFragment\n  id\n  mcpId\n  copyrightNotice\n  language\n  ratings {\n    ratingValue\n    ratingSubValues\n    ratingSourceLink\n    __typename\n  }\n  contributors {\n    name\n    slug\n    roles\n    __typename\n  }\n  copyrightOwners {\n    name\n    __typename\n  }\n  videoType\n  videoTypeData {\n    ...VideoTypeMovieFullFragment\n    ...VideoTypeEpisodeFullFragment\n    ...VideoTypeSeriesFullFragment\n    ...VideoTypeExtraBasicFragment\n    __typename\n  }\n  detailPageMetadata {\n    uploadDate\n    breadcrumbs {\n      title\n      urlPath\n      __typename\n    }\n    __typename\n  }\n  detailPageAnalyticsMetadata {\n    ...AnalyticsTrackingMetadataFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ImageAssetFragment on ImageAsset {\n  filePath\n  imageRole\n  link\n  mediaType\n  __typename\n}\n\nfragment VideoContentBasicFragment on VideoContent {\n  id\n  copyrightYear\n  dateReleased\n  description\n  genresV2 {\n    name\n    slug\n    __typename\n  }\n  headline\n  keywords\n  title\n  badges\n  contentVertical\n  ratings {\n    ratingValue\n    __typename\n  }\n  imageAssets {\n    ...ImageAssetFragment\n    __typename\n  }\n  videoType\n  videoTypeData {\n    ...VideoTypeMovieBasicFragment\n    ...VideoTypeSeriesBasicFragment\n    ...VideoTypeEpisodeBasicFragment\n    __typename\n  }\n  vodAvailability {\n    isBlocked\n    reason\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeMovieBasicFragment on VideoTypeMovieData {\n  playbackData {\n    streamMetadata {\n      duration\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeSeriesBasicFragment on VideoTypeSeriesData {\n  seriesSubType\n  seasonsCount\n  episodesCount\n  __typename\n}\n\nfragment VideoTypeEpisodeBasicFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n    streamMetadata {\n      duration\n      __typename\n    }\n    __typename\n  }\n  season {\n    id\n    title\n    yearReleased\n    __typename\n  }\n  series {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeMovieFullFragment on VideoTypeMovieData {\n  playbackData {\n    streamMetadata {\n      duration\n      introStartPosition\n      introEndPosition\n      outroStartPosition\n      __typename\n    }\n    trackingMetadata(navigationSection: $navigationSection) {\n      ...TrackingMetadataFragment\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TrackingMetadataFragment on VideoPlaybackTrackingData {\n  advertisingMetadata {\n    adUnit\n    keyValues {\n      key\n      value\n      __typename\n    }\n    adConfiguration\n    __typename\n  }\n  analyticsMetadata {\n    keyValues {\n      key\n      value\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeSeriesFullFragment on VideoTypeSeriesData {\n  seriesSubType\n  seasonsCount\n  episodesCount\n  currentSeason {\n    id\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeEpisodeFullFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n    streamMetadata {\n      duration\n      introStartPosition\n      introEndPosition\n      outroStartPosition\n      __typename\n    }\n    trackingMetadata(navigationSection: $navigationSection) {\n      ...TrackingMetadataFragment\n      __typename\n    }\n    __typename\n  }\n  series {\n    id\n    title\n    __typename\n  }\n  season {\n    id\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeExtraBasicFragment on VideoTypeExtraData {\n  extraType\n  playbackData {\n    streamMetadata {\n      duration\n      __typename\n    }\n    __typename\n  }\n  ... on VideoTypeExtraData {\n    parents {\n      id\n      vodAvailability {\n        isBlocked\n        reason\n        __typename\n      }\n      title\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment AnalyticsTrackingMetadataFragment on AnalyticsTrackingMetadata {\n  keyValues {\n    key\n    value\n    __typename\n  }\n  __typename\n}\n\nfragment SeasonsConnectionFragment on VideoTypeSeriesData {\n  seasonsConnection(pagination: $pagination) {\n    totalCount\n    edges {\n      cursor\n      node {\n        id\n        title\n        yearReleased\n        episodesConnection(pagination: {first: null, after: null}) {\n          edges {\n            node {\n              id\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      ...PageInfoFragment\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PageInfoFragment on PageInfo {\n  hasPreviousPage\n  hasNextPage\n  startCursor\n  endCursor\n  __typename\n}\n\nfragment PageMetadataFragment on PageMetadata {\n  title\n  description\n  canonicalUrl\n  altUrls\n  uploadDate\n  twitter {\n    card\n    site\n    description\n    title\n    image\n    imageAlt\n    __typename\n  }\n  og {\n    title\n    type\n    image {\n      url\n      type\n      width\n      height\n      alt\n      __typename\n    }\n    url\n    description\n    siteName\n    locale\n    localeAlternative\n    __typename\n  }\n  breadcrumbs {\n    title\n    urlPath\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeExtraFullFragment on VideoTypeExtraData {\n  playbackData {\n    streamMetadata {\n      duration\n      introStartPosition\n      introEndPosition\n      outroStartPosition\n      __typename\n    }\n    trackingMetadata(navigationSection: $navigationSection) {\n      ...TrackingMetadataFragment\n      __typename\n    }\n    __typename\n  }\n  __typename\n}',
        },
        headers={
            'authority': 'client-api.vix.com',
            'origin': 'https://www.vix.com',
            'referer': 'https://www.vix.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3',
            'x-vix-api-key': '8r23XTUiE2SsR7hL19qzIqg0XULLV6FkbuXWVmii1y906aSz',
            'x-vix-device-type': 'desktop',
            'x-vix-platform': 'web',
        })
        if r.status_code != 200:
            raise Exception(r.text)
        return r.json()
    def get_movie(self, movie_id: str) -> dict:
        r = self.session.post(url=f"https://tkx.mp.lura.live/rest/v2/mcp/video/{movie_id}/metadata",
            headers={
                'authority': 'tkx.mp.lura.live',
                'accept': '*/*',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4,ja;q=0.3,de;q=0.2',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://vix.com',
                'referer': 'https://vix.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            },
            params = {
                'anvack': 'GAmN765ORsrVpoGIW6Ik9pB7CqVjJx4j',
                'anvtrid': 'wf18cecea1fcf66a54651ea6d75f5634f',
                'rtyp': 'fp',
                'X-Anvato-Adst-Auth': 'UB9eGXlfMR7XVZ9QpoFyI8xGOUK1e8gXqwnDtdhZkpRN0V7CI7m6aRmTiWipD1gj7VeaoYAkdmjxV8OjP6CcCQ==',
            },
        )
        if r.status_code != 200:
            raise Exception(r.text)
        return r.json()

    def get_metadata(self, content_id: str) -> dict:
        r = self.session.post(url='https://client-api.vix.com/gql/v1/',
        json={
            "operationName": "VideoData",
            "variables": {
                "id": f"video:mcp:{content_id}",
                "navigationSection": {
                    "urlPath": '',
                    "pageItemId": ''
                },
                'pagination': {
                    'first': None,
                    'after': None,
                },
                'seasonsConnectionSeriesPagination': {
                    'first': None,
                    'after': None,
                },
                'episodesConnectionSeriesPagination': {
                    'first': 1,
                    'after': None,
                },
            },
            'query': 'query VideoData($id: ID!, $navigationSection: TrackingNavigationSectionInput!, $pagination: PaginationParams!, $seasonsConnectionSeriesPagination: PaginationParams!, $episodesConnectionSeriesPagination: PaginationParams!) {\n  videoById(id: $id) {\n    detailPageMetadata {\n      ...PageMetadataFragment\n      __typename\n    }\n    vodAvailability {\n      isBlocked\n      reason\n      __typename\n    }\n    ...VideoContentFullFragment\n    videoTypeData {\n      ...VideoTypeMovieFullFragment\n      ... on VideoTypeExtraData {\n        ...VideoTypeExtraFullFragment\n        __typename\n      }\n      ... on VideoTypeSeriesData {\n        ...VideoTypeSeriesFullFragment\n        ...SeasonsConnectionFragment\n        __typename\n      }\n      ... on VideoTypeEpisodeData {\n        ...VideoTypeEpisodeFullFragment\n        series {\n          id\n          title\n          videoTypeData {\n            ... on VideoTypeSeriesData {\n              episodesCount\n              seasonsConnection(pagination: $seasonsConnectionSeriesPagination) {\n                edges {\n                  node {\n                    id\n                    title\n                    episodesConnection(pagination: $episodesConnectionSeriesPagination) {\n                      edges {\n                        node {\n                          id\n                          videoTypeData {\n                            ...VideoTypeEpisodeBasicTrackingFragment\n                            __typename\n                          }\n                          __typename\n                        }\n                        __typename\n                      }\n                      __typename\n                    }\n                    __typename\n                  }\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        season {\n          id\n          title\n          episodesConnection(pagination: $pagination) {\n            totalCount\n            edges {\n              cursor\n              node {\n                id\n                videoTypeData {\n                  ...VideoTypeEpisodeBasicTrackingFragment\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment VideoContentFullFragment on VideoContent {\n  ...VideoContentBasicFragment\n  id\n  mcpId\n  copyrightNotice\n  language\n  ratings {\n    ratingValue\n    ratingSubValues\n    ratingSourceLink\n    __typename\n  }\n  contributors {\n    name\n    slug\n    roles\n    __typename\n  }\n  copyrightOwners {\n    name\n    __typename\n  }\n  videoType\n  videoTypeData {\n    ...VideoTypeMovieFullFragment\n    ...VideoTypeEpisodeFullFragment\n    ...VideoTypeSeriesFullFragment\n    ...VideoTypeExtraBasicFragment\n    __typename\n  }\n  detailPageMetadata {\n    uploadDate\n    breadcrumbs {\n      title\n      urlPath\n      __typename\n    }\n    __typename\n  }\n  detailPageAnalyticsMetadata {\n    ...AnalyticsTrackingMetadataFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ImageAssetFragment on ImageAsset {\n  filePath\n  imageRole\n  link\n  mediaType\n  __typename\n}\n\nfragment VideoContentBasicFragment on VideoContent {\n  id\n  copyrightYear\n  dateReleased\n  description\n  genresV2 {\n    name\n    slug\n    __typename\n  }\n  headline\n  keywords\n  title\n  badges\n  contentVertical\n  ratings {\n    ratingValue\n    __typename\n  }\n  imageAssets {\n    ...ImageAssetFragment\n    __typename\n  }\n  videoType\n  videoTypeData {\n    ...VideoTypeMovieBasicFragment\n    ...VideoTypeSeriesBasicFragment\n    ...VideoTypeEpisodeBasicFragment\n    __typename\n  }\n  vodAvailability {\n    isBlocked\n    reason\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeMovieBasicFragment on VideoTypeMovieData {\n  playbackData {\n    streamMetadata {\n      duration\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeSeriesBasicFragment on VideoTypeSeriesData {\n  seriesSubType\n  seasonsCount\n  episodesCount\n  __typename\n}\n\nfragment VideoTypeEpisodeBasicFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n    streamMetadata {\n      duration\n      __typename\n    }\n    __typename\n  }\n  season {\n    id\n    title\n    yearReleased\n    __typename\n  }\n  series {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeMovieFullFragment on VideoTypeMovieData {\n  playbackData {\n    streamMetadata {\n      duration\n      introStartPosition\n      introEndPosition\n      outroStartPosition\n      __typename\n    }\n    trackingMetadata(navigationSection: $navigationSection) {\n      ...TrackingMetadataFragment\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TrackingMetadataFragment on VideoPlaybackTrackingData {\n  advertisingMetadata {\n    adUnit\n    keyValues {\n      key\n      value\n      __typename\n    }\n    adConfiguration\n    __typename\n  }\n  analyticsMetadata {\n    keyValues {\n      key\n      value\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeSeriesFullFragment on VideoTypeSeriesData {\n  seriesSubType\n  seasonsCount\n  episodesCount\n  currentSeason {\n    id\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeEpisodeFullFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n    streamMetadata {\n      duration\n      introStartPosition\n      introEndPosition\n      outroStartPosition\n      __typename\n    }\n    trackingMetadata(navigationSection: $navigationSection) {\n      ...TrackingMetadataFragment\n      __typename\n    }\n    __typename\n  }\n  series {\n    id\n    title\n    __typename\n  }\n  season {\n    id\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeExtraBasicFragment on VideoTypeExtraData {\n  extraType\n  playbackData {\n    streamMetadata {\n      duration\n      __typename\n    }\n    __typename\n  }\n  ... on VideoTypeExtraData {\n    parents {\n      id\n      vodAvailability {\n        isBlocked\n        reason\n        __typename\n      }\n      title\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment AnalyticsTrackingMetadataFragment on AnalyticsTrackingMetadata {\n  keyValues {\n    key\n    value\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeEpisodeBasicTrackingFragment on VideoTypeEpisodeData {\n  ...VideoTypeEpisodeBasicFragment\n  playbackData {\n    trackingMetadata(navigationSection: $navigationSection) {\n      ...TrackingMetadataFragment\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PageMetadataFragment on PageMetadata {\n  title\n  description\n  canonicalUrl\n  altUrls\n  uploadDate\n  twitter {\n    card\n    site\n    description\n    title\n    image\n    imageAlt\n    __typename\n  }\n  og {\n    title\n    type\n    image {\n      url\n      type\n      width\n      height\n      alt\n      __typename\n    }\n    url\n    description\n    siteName\n    locale\n    localeAlternative\n    __typename\n  }\n  breadcrumbs {\n    title\n    urlPath\n    __typename\n  }\n  __typename\n}\n\nfragment SeasonsConnectionFragment on VideoTypeSeriesData {\n  seasonsConnection(pagination: $pagination) {\n    totalCount\n    edges {\n      cursor\n      node {\n        id\n        title\n        yearReleased\n        episodesConnection(pagination: {first: null, after: null}) {\n          edges {\n            node {\n              id\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      ...PageInfoFragment\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PageInfoFragment on PageInfo {\n  hasPreviousPage\n  hasNextPage\n  startCursor\n  endCursor\n  __typename\n}\n\nfragment VideoTypeExtraFullFragment on VideoTypeExtraData {\n  playbackData {\n    streamMetadata {\n      duration\n      introStartPosition\n      introEndPosition\n      outroStartPosition\n      __typename\n    }\n    trackingMetadata(navigationSection: $navigationSection) {\n      ...TrackingMetadataFragment\n      __typename\n    }\n    __typename\n  }\n  __typename\n}',
        },
        headers={
            'authority': 'client-api.vix.com',
            'origin': 'https://www.vix.com',
            'referer': 'https://www.vix.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3',
            'x-vix-api-key': '8r23XTUiE2SsR7hL19qzIqg0XULLV6FkbuXWVmii1y906aSz',
            'x-vix-device-type': 'desktop',
            'x-vix-platform': 'web',
        })
        if r.status_code != 200:
            raise Exception(r.text)
        return r.json()

    def get_media(self, media_id: str) -> dict:
        r = self.session.get(url='https://vix.com/api/video/token',
            headers = {
                'authority': 'vix.com',
                'accept': '*/*',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4,ja;q=0.3,de;q=0.2',
                'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMyOTgwNDkiLCJhcCI6IjExMjgzMDQ4MDYiLCJpZCI6ImJjZTE3ZGJhODJiM2FmYmQiLCJ0ciI6IjA2NWFjYzhiOTlhOWNmNmY4NTk5MmY3YThiOGY2MzUwIiwidGkiOjE2NzY5MzQ0ODMzMjh9fQ==',
                'referer': 'https://vix.com/es-es/detail/video-4147109',
                'traceparent': '00-065acc8b99a9cf6f85992f7a8b8f6350-bce17dba82b3afbd-01',
                'tracestate': '3298049@nr=0-1-3298049-1128304806-bce17dba82b3afbd----1676934483328',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                'x-video-type': 'VOD',
            },
            params = {
                'videoId': media_id,
                'timestamp': int(time.time()),
            }
        )
        if r.status_code != 200:
            raise Exception(r.text)
        res = self.session.post(url=f'https://tkx.mp.lura.live/rest/v2/mcp/video/{media_id}',
            headers = {
                'authority': 'tkx.mp.lura.live',
                'accept': '*/*',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4,ja;q=0.3,de;q=0.2',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://vix.com',
                'referer': 'https://vix.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            },
            params = {
                'anvack': r.json()["accessKey"],
                'rtyp':'fp'
            },
            json = {
                "content":{
                    "mcp_video_id": str(media_id),
                },
                "user": {
                    "device":"android",
                    "device_id":"2890d349-8514-4650-832e-11e1735420a6",
                },
                "api": {
                    "anvts": int(time.time()),
                    "anvstk2": r.json()["token"],
                }
            }
        )
        if r.status_code != 200:
            raise Exception(res.text)
        res = res.text
        res = res.replace('anvatoVideoJSONLoaded(','').replace(')','')
        res = json.loads(res)
        for i in res['published_urls']:
            if i['format'].lower() == 'dash':
                mpd_url = i['embed_url']
                self.license_url = i['license_url']
                break
        mpd = self.session.get(mpd_url)
        return mpd.json()["master_m3u8"], res['captions']