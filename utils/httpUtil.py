import requests


class HttpUtil:

    def get(self, url, header):
        requests.get()
        return

    def post(self, url, data, headers, timeout):
        response = requests.post(url, data=data, headers=headers, timeout=timeout)
        result = response.text
        return
