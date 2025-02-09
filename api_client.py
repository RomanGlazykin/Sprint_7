import requests
import json

class ApiClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout

    def post(self, path, data=None, headers=None):
        url = self.base_url + path
        default_headers = {'Content-Type': 'application/json'}
        if headers:
            default_headers.update(headers)

        try:
            response = requests.post(url, data=json.dumps(data), headers=default_headers, timeout=self.timeout)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get(self, path, params=None, headers=None):
        url = self.base_url + path
        try:
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def delete(self, path, headers=None):
        url = self.base_url + path
        try:
            response = requests.delete(url, headers=headers, timeout=self.timeout)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None