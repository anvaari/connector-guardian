class RequestFailedError(Exception):
    def __init__(self, url):
        self.url = url
        super().__init__(f"Failed to make a successful request to {url}")
