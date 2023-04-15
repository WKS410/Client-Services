import requests

API_URL = 'https://app-api.tvgo.americatv.com.pe/v2/gql'
TOKEN_FILE = 'token.json'

HEADERS = {
    'Connection': 'Keep-Alive',
    'Host': 'app-api.tvgo.americatv.com.pe',
    'User-Agent': 'okhttp/4.9.2',
}

def AmericaTVGOClient():
    url = input("Enter Url Eps: ")
    episode_id = get_episode_id(url)
    episode_info = get_episode_info(episode_id)
    print_episode_info(episode_info)

def get_episode_id(url):
    return url.split("-")[-1].split("#")[-2]

def get_episode_info(episode_id):
    query = '''
        query ($mediaProvider: MediaProviderEnum!, $imageSize: String!, $imageType: ImageTypeEnum!, $chaptersSort: SortEnum!, $chapterFirst: Int!, $metadataType: MetadataTypeEnum!, $showSlug: String!, $seasonSlug: String!) {
            show(slug: $showSlug) {
                season(slug: $seasonSlug) {
                    chapters(first: $chapterFirst, sort: $chaptersSort) {
                        cursor
                        node {
                            free
                            slug
                            title
                            duration
                            images(imageType: $imageType) {
                                url(size: $imageSize)
                            }
                            media(provider: $mediaProvider) {
                                mediaId
                            }
                            metadata(metadataType: $metadataType) {
                                value
                            }
                        }
                    }
                }
            }
        }
    '''
    variables = {
        'mediaProvider': 'MEDIASTREAM',
        'imageSize': '300x300',
        'imageType': 'POSTER',
        'chaptersSort': 'SORT_ASC',
        'chapterFirst': 10,
        'metadataType': 'VAST_ANDROID',
        'showSlug': '1-series-tvgo',
        'seasonSlug': '1-series-tvgo/3-es-lo-que-hay/1-temporada-1',
    }
    response = requests.post(API_URL, json={'query': query, 'variables': variables}, headers=HEADERS)
    data = response.json()
    episodes = data['data']['show']['season']['chapters']['node']
    for episode in episodes:
        if episode['media'][0]['mediaId'] == episode_id:
            return episode
    return None

def print_episode_info(episode_info):
    if episode_info is None:
        print('Episode not found')
        return
    title = episode_info['title']
    images = episode_info['images']
    duration = episode_info['duration']
    access_token = get_access_token(episode_info['media'][0]['mediaId'])
    hls_url = 'https://mdstrm.com/video/{}.m3u8?access_token={}'.format(episode_info['media'][0]['mediaId'], access_token)
    print('')
    print('-' * 50)
    print(f'TITLE: {title}')
    print(f'DURATION: {duration}')
    print(f'IMAGES:')
    for image in images:
        print(f'\t{image["url"]}')
    print(f'M3U8 URL: {hls_url}') 

def get_access_token(media_id):
    headers = {
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'app-api.tvgo.americatv.com.pe',
        'User-Agent': 'okhttp/4.9.2',
    }
    data = {
        'media_id': media_id,
        'type': 'tvgo',
    }
    response = requests.post('https://app-api.tvgo.americatv.com.pe/v2/mediaToken', headers=headers, data=data)
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        with open(TOKEN_FILE, 'w') as f:
            json.dump({'access_token': access_token}, f)
        return access_token
    elif response.status_code == 400:
        raise ValueError('Invalid request. Check media_id and type')
    elif response.status_code == 401:
        raise ValueError('Authentication failed. Check your credentials')
    elif response.status_code == 403:
        raise ValueError('Access denied. Check your permissions')
    else:
        raise ValueError(f'Request failed with status code {response.status_code}')