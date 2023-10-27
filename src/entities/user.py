import io
import os

from requests_toolbelt.downloadutils import stream

from adiauthcli import Client

from src.enums import Visibility
from src.exceptions import InvalidTokenError, UnknownError, NotLoggedIn, BlobNotFoundError
from ._api_requester import _ApiRequester


_auth_url_ = os.getenv("AUTH_URL", "http://localhost:3001/")

class User(Client, _ApiRequester):

    @property
    def blobs(self) -> list[str]:
        res = self._do_request(
            "GET",
            endpoint="blobs/")

        if res.status_code == 401:
            raise InvalidTokenError
        if res.status_code == 200:
            return [
                blob_info["blobId"]
                for blob_info
                in res.json()["blobs"]]

        raise UnknownError(res.content)

    @property
    def username(self) -> str:
        return self._user_

    def __init__(self, admin_token: str | None = None):
        super().__init__(_auth_url_, admin_token)

    def new_blob(
            self,
            visibility: Visibility = Visibility.PRIVATE,
            content: io.BytesIO = None) -> str:
        if self._token_ is None:
            raise NotLoggedIn

        res = self._do_request(
            "POST",
            endpoint="blobs/",
            json={
                "visibility": visibility.value
            })

        if res.status_code == 401:
            raise InvalidTokenError
        if res.status_code == 201:
            blob_id = res.json()["blobId"]

            if content is not None:
                self.upload(blob_id, content)

            return blob_id

        raise UnknownError(res.content)

    def upload(self, blob_id: str, content: io.BufferedReader) -> None:
        res = self._do_request(
            "PUT",
            endpoint=f"blobs/{blob_id}",
            data=content)

        if res.status_code == 404:
            raise BlobNotFoundError
        if res.status_code == 204:
            return

        raise UnknownError(res.content)

    def delete(self, blob_id: str) -> None:
        res = self._do_request(
            "DELETE",
            endpoint=f"blobs/{blob_id}")

        if res.status_code == 404:
            raise BlobNotFoundError
        if res.status_code == 204:
            return

        raise UnknownError(res.content)

    def hash(self, blob_id: str, *types) -> dict[str, str]:
        if not types:
            raise ValueError("No hash types provided")

        res = self._do_request(
            "GET",
            endpoint=f"blobs/{blob_id}/hash?type={",".join(types)}")

        if res.status_code == 404:
            raise BlobNotFoundError
        if res.status_code == 200:
            return res.json()

        raise UnknownError(res.content)

    def download(self, blob_id: str, path: os.PathLike | str = None) -> os.PathLike:
        res = self._do_request(
            "GET",
            endpoint=f"blobs/{blob_id}",
            stream=True
        )

        _path = path if path is not None else os.path.join(os.getcwd(), blob_id)

        if res.status_code == 404:
            raise BlobNotFoundError(blob_id)
        if res.status_code == 200:
            return stream.stream_response_to_file(res, _path, chunksize=1024 * 1024)

        raise UnknownError(res.content)

    def exists(self, blob_id: str) -> bool:
        res = self._do_request(
            "HEAD",
            endpoint=f"blobs/{blob_id}")

        if res.status_code == 200:
            return True
        if res.status_code == 404:
            return False

        raise UnknownError(res.content)
