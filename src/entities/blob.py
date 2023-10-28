import os

from requests_toolbelt.downloadutils import stream

from ._apiRequester import _ApiRequester
from src.enums import Visibility
from src.exceptions import BlobNotFoundError, NotLoggedIn, UnknownError


class Blob(_ApiRequester):

    @property
    def accessURL(self) -> str:
        return f"{self.serviceURL}/api/v1/blobs/{self.blobId}"

    @property
    def isPrivate(self) -> bool:
        return self._visibility == Visibility.PRIVATE

    @property
    def md5(self) -> str:
        return self._hash("md5")["md5"]

    @property
    def sha256(self) -> str:
        return self._hash("sha256")["sha256"]

    def __init__(self, blobId: str, authToken: str = None):
        super().__init__(authToken)
        self.blobId = blobId
        self._visibility = Visibility.PRIVATE
        self.allowedUsers = []

    def _hash(self, *types) -> dict[str, str]:
        if not types:
            raise ValueError("No hash types specified")

        res = self._do_request(
            "GET",
            endpoint=f"blobs/{self.blobId}/hash",
            params={
                "type": ",".join(types)
            }
        )

        if res.status_code == 404:
            raise BlobNotFoundError(self.blobId)
        if res.status_code == 200:
            return res.json()

        raise UnknownError(res.content)

    def allowUser(self, username: str) -> None:
        if not self.authToken:
            raise NotLoggedIn

        res = self._do_request(
            "PATCH",
            endpoint=f"blobs/{self.blobId}/acl",
            json={
                "acl": [
                    username
                ]
            })

        if res.status_code == 404:
            raise BlobNotFoundError(self.blobId)
        if res.status_code == 204:
            return

        raise UnknownError(res.content)

    def delete(self) -> None:
        if not self.authToken:
            raise NotLoggedIn

        res = self._do_request(
            "DELETE",
            endpoint=f"blobs/{self.blobId}")

        if res.status_code == 404:
            raise BlobNotFoundError(self.blobId)
        if res.status_code == 204:
            return

        raise UnknownError(res.content)

    def dumpToFile(self, localFilename: str | os.PathLike = None) -> None:
        res = self._do_request(
            "GET",
            endpoint=f"blobs/{self.blobId}",
            stream=True)

        if res.status_code == 404:
            raise BlobNotFoundError(self.blobId)
        if res.status_code == 200:
            filename = localFilename if localFilename is not None else self.blobId
            with open(filename, "wb") as f:
                stream.stream_response_to_file(res, f, chunksize = 1024 * 1024)
            return

        raise UnknownError(res.content)

    def revokeUser(self, username: str) -> None:
        if not self.authToken:
            raise NotLoggedIn

        res = self._do_request(
            "DELETE",
            endpoint=f"blobs/{self.blobId}/acl/{username}")

        if res.status_code == 404:
            raise BlobNotFoundError(self.blobId)
        if res.status_code == 204:
            return

        raise UnknownError(res.content)

    def setVisibility(self, private: bool) -> None:
        if not self.authToken:
            raise NotLoggedIn

        res = self._do_request(
            "PUT",
            endpoint=f"blobs/{self.blobId}/visibility",
            json={
                "visibility": Visibility.PRIVATE.value if private else Visibility.PUBLIC.value
            })

        if res.status_code == 404:
            raise BlobNotFoundError(self.blobId)
        if res.status_code == 204:
            return

        raise UnknownError(res.content)

    def uploadFromFile(self, localFilename: str | os.PathLike) -> None:
        if not self.authToken:
            raise NotLoggedIn

        with open(localFilename, "rb") as f:
            res = self._do_request(
                "PUT",
                endpoint=f"blobs/{self.blobId}",
                data=f)

        if res.status_code == 404:
            raise BlobNotFoundError(self.blobId)
        if res.status_code == 204:
            return

        raise UnknownError(res.content)
