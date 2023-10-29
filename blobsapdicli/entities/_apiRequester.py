import requests


class _ApiRequester:

    serviceURL: str = "http://localhost:3001"

    def __init__(self, authToken: str = None, serviceURL: str = None):
        _ApiRequester.serviceURL = serviceURL.rstrip("/") \
            if serviceURL is not None \
            else _ApiRequester.serviceURL
        self.authToken = authToken

    def _do_request(
        self,
        method: str,
        /,
        *args,
        endpoint: str = "",
        **kwargs) -> requests.Response:

        headers = kwargs.pop("headers", None)

        headers = { } if headers is None else headers
        _headers = { } if self.authToken is None else { "AuthToken": self.authToken }

        headers.update(_headers)

        return requests.request(
            method=method,
            url=f"{self.serviceURL}/api/v1/{endpoint}",
            timeout=5,
            headers=headers,
            *args,
            **kwargs)
