import os
import requests


_blob_url_ = os.getenv("BLOB_URL", "http://localhost:3002/api/v1/")

class _ApiRequester:

    _token_: str | None

    def _do_request(
            self,
            method: str,
            /,
            *args,
            endpoint: str = "",
            **kwargs) -> requests.Response:

        headers = kwargs.pop("headers", None)

        headers = { } if headers is None else headers
        _headers = { } if self._token_ is None else { "AuthToken": self._token_ }

        headers.update(_headers)

        return requests.request(
            method=method,
            url=f"{_blob_url_}{endpoint}",
            timeout=5,
            headers=headers,
            *args,
            **kwargs)

__export__ = {_ApiRequester}
