import requests
import json
import time
import toml


class BraviaCOREClient:
    def __init__(self, ip_address, psk):
        self.ip_address = ip_address
        self.psk = psk

    def _get_headers(self):
        return {
            'X-Auth-PSK': self.psk,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }

    def _get_url(self, endpoint):
        return f'http://{self.ip_address}:80/sony/{endpoint}'

    def send_command(self, cmd, params=None):
        endpoint = 'system'
        url = self._get_url(endpoint)
        headers = self._get_headers()

        if params:
            params = [{"name": x, "value": y} for x, y in params.items()]
        else:
            params = []

        data = {
            'id': 20,
            'method': 'actRegister',
            'version': '1.0',
            'params': [
                {
                    'clientid': 'Sonymote',
                    'nickname': 'python',
                    'level': 'private'
                },
                [
                    {
                        'value': 'yes',
                        'function': 'WOL'
                    },
                    {
                        'value': 'yes',
                        'function': 'IRCC'
                    }
                ]
            ]
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=5)
            if response.status_code == 200:
                reg = response.json()
                if 'result' in reg:
                    if '0' in reg['result'][1]:
                        endpoint = 'avContent'
                        url = self._get_url(endpoint)
                        headers = self._get_headers()
                        params = [
                            {"name": "scheme", "value": "byRemote"},
                            {"name": "byRemote", "value": "1.0"},
                            {"name": "resource", "value": f"command/{cmd}"},
                            {"name": "category", "value": "system"}
                        ] + params
                        data = {
                            'method': 'setPlayContent',
                            'params': params,
                            'id': 2,
                            'version': '1.0'
                        }
                        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=5)
                        if response.status_code == 200:
                            return response.json()['result'][1]
                        else:
                            raise Exception(f'Response returned: {response.status_code}')
                    else:
                        raise Exception('Could not register')
                else:
                    raise Exception('Unexpected response')
            else:
                raise Exception(f'Response returned: {response.status_code}')
        except requests.exceptions.RequestException as e:
            raise Exception(f'Request failed: {e}')

    def volume_up(self):
        return self.send_command('VolumeUp')

    def volume_down(self):
        return self.send_command('VolumeDown')

    def set_volume_level(self, level):
        return self.send_command('SetVolume', params={'volume': f'{level}%'})

    def get_volume_info(self):
        return self.send_command('GetVolumeInformation')

    def set_input(self, input_source):
        return self.send_command('SetInput', params={'uri': f'extInput:{input_source}'})

    def power_on(self):
        return self.send_command('PowerOn')

    def power_off(self):
        return self.send_command('PowerOff')

