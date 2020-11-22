import requests


class RequestConfiguration:
    headers = {}
    payload = {}

    def __init__(self, url, method="GET"):
        self.url = url
        self.method = method

    # Create and execute http request
    def create(self):
        return requests.request(self.method, self.url, headers=self.headers, data=self.payload)
