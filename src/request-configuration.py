
class RequestConfiguration:
    headers = []

    def __init__(self, url, method="GET"):
        self.url = url
        self.method = method
