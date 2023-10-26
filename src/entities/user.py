import io
import os

from adiauthcli import Client

from src.enums import Visibility
from src.exceptions import InvalidTokenError, UnknownError, NotLoggedIn
from ._api_requester import _ApiRequester
from .blob import _UserBlob


_auth_url_ = os.getenv("AUTH_URL", "http://localhost:3001/")

class User(Client, _ApiRequester):

    @property
    def blobs(self) -> list['_UserBlob']:
        res = self._do_request(
            "GET",
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

    def new_blob(
            self,
            visibility: Visibility = Visibility.PRIVATE,
            content: io.BytesIO = None) -> '_UserBlob':
        if self._token_ is None:
            raise NotLoggedIn

        res = self._do_request(
            "POST",
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
