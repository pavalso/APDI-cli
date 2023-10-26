import io
import os

import requests
from requests_toolbelt.downloadutils import stream

from adiauthcli import Client
from enums import Visibility
from exceptions import InvalidTokenError, NotLoggedIn, UnknownError, BlobNotFoundError


_blob_url_ = os.getenv("BLOB_URL", "http://localhost:3002/api/v1/")
_auth_url_ = os.getenv("AUTH_URL", "http://localhost:3001/")

class User(Client):

    @property
    def blobs(self) -> list['_UserBlob']:
        res = self._do_request(
            method="GET",
            endpoint="blobs/")

        if res.status_code == 401:
            raise InvalidTokenError
        if res.status_code == 200:
            return [
                _UserBlob(blob_info["blobId"], self._token_)
                for blob_info 
                in res.json()["blobs"]]

        raise UnknownError(res.content)

    def __init__(self, admin_token: str | None = None):
        super().__init__(_auth_url_, admin_token)

    def _do_request(
            self,
            method: str,
            endpoint: str,
            json: dict = None,
            headers: dict = None,
            content: io.TextIOWrapper = None,
            stream_: bool = False) -> requests.Response:

        headers = { } if headers is None else headers
        _headers = { } if self._token_ is None else { "AuthToken": self._token_ }

        headers.update(_headers)

        return requests.request(
            method=method,
            url=f"{_blob_url_}{endpoint}",
            json=json,
            headers=headers,
            data=content,
            stream=stream_,
            timeout=5)

    def create_blob(
            self,
            visibility: Visibility = Visibility.PRIVATE,
            content: io.BytesIO = None) -> '_UserBlob':
        if self._token_ is None:
            raise NotLoggedIn

        res = self._do_request(
            method="POST",
            endpoint="blobs/",
            json={
                "visibility": visibility
            })

        if res.status_code == 401:
            raise InvalidTokenError
        if res.status_code == 201:
            blob_id = res.json()["blobId"]
            blob = _UserBlob(blob_id, self._token_)

            if content is not None:
                blob.upload(content)

            return blob

        raise UnknownError(res.content)

class _UserBlob:

    def __init__(self, id_: str, user_token: str) -> None:
        self.id_ = id_
        self._token_ = user_token

    def _do_request(
            self,
            method: str,
            endpoint: str = "",
            json: dict = None,
            headers: dict = None,
            content: io.TextIOWrapper = None,
            stream_: bool = False) -> requests.Response:

        headers = { } if headers is None else headers
        _headers = { "AuthToken": self._token_ }

        headers.update(_headers)

        endpoint = self.id_ if not endpoint else f"{self.id_}/{endpoint}"

        return requests.request(
            method=method,
            url=f"{_blob_url_}blobs/{endpoint}",
            json=json,
            headers=headers,
            data=content,
            stream=stream_,
            timeout=5)

    def download(self, path: os.PathLike | str = None) -> os.PathLike:
        res = self._do_request(
            method="GET",
            stream_=True
        )

        _path = path if path is not None else os.path.join(os.getcwd(), self.id_)

        if res.status_code == 404:
            raise BlobNotFoundError(self.id_)
        if res.status_code == 200:
            return stream.stream_response_to_file(res, _path, chunksize=1024 * 1024)

        raise UnknownError(res.content)

    def upload(self, content: io.BufferedReader) -> None:
        res = self._do_request(
            method="PUT",
            content=content)

        if res.status_code == 401:
            raise InvalidTokenError
        if res.status_code == 204:
            return

        raise UnknownError(res.content)

    def delete(self) -> None:
        res = self._do_request(
            method="DELETE")

        if res.status_code == 401:
            raise InvalidTokenError
        if res.status_code == 204:
            return

        raise UnknownError(res.content)
