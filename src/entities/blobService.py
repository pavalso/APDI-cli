import os

from src.enums import Visibility
from src.exceptions import BlobNotFoundError, InvalidTokenError, UnknownError, NotLoggedIn
from .blob import Blob
from ._apiRequester import _ApiRequester


class BlobService(_ApiRequester):

    def __init__(self, serviceURL: str, authToken: str = None) -> None:
        super().__init__(authToken, serviceURL)

    def createBlob(self, localFilename: str | os.PathLike) -> Blob:
        if self.authToken is None:
            raise NotLoggedIn

        res = self._do_request(
            "POST",
            endpoint="blobs",
            json={
                "visibility": Visibility.PRIVATE.value
            }
        )

        if res.status_code == 401:
            raise InvalidTokenError
        if res.status_code == 201:
            blob = Blob(res.json()["blobId"], self.authToken)

            blob.uploadFromFile(localFilename)

            return blob

        raise UnknownError(res.content)

    def deleteBlob(self, blob: str | Blob) -> None:
        if self.authToken is None:
            raise NotLoggedIn

        res = self._do_request(
            "DELETE",
            endpoint=f"blobs/{blob.blobId}"
        )

        if res.status_code == 404:
            raise BlobNotFoundError(blob.blobId)
        if res.status_code == 204:
            return

        raise UnknownError(res.content)

    def getBlob(self, blobId: str) -> Blob:
        res = self._do_request(
            "GET",
            endpoint=f"blobs/{blobId}"
        )

        if res.status_code == 404:
            raise BlobNotFoundError(blobId)
        if res.status_code == 200:
            blob = Blob(blobId, self.authToken)
            return blob

        raise UnknownError(res.content)

    def getBlobs(self) -> list[str]:
        if self.authToken is None:
            raise NotLoggedIn

        res = self._do_request(
            "GET",
            endpoint="blobs/"
        )

        if res.status_code == 401:
            raise InvalidTokenError
        if res.status_code == 200:
            return [
                blob_info["blobId"]
                for blob_info
                in res.json()["blobs"]
                ]

        raise UnknownError(res.content)
