import os

from requests_toolbelt.downloadutils import stream

from src.enums import Visibility
from src.exceptions import InvalidBlob, BlobServiceError
from ._apiRequester import _ApiRequester


class Blob(_ApiRequester):

    @property
    def accessURL(self) -> str:
        return f"{self.serviceURL}/api/v1/blobs/{self.blobId}"

    @property
    def endpoint(self) -> str:
        return f"blobs/{self.blobId}"

    @property
    def allowedUsers(self) -> list[str]:
        res = self._do_request(
            "GET",
            endpoint=f"{self.endpoint}/acl")

        if res.status_code == 404:
            raise InvalidBlob
        if res.status_code == 200:
            return res.json()["allowed_users"]
        if res.status_code == 204:
            return []

        raise BlobServiceError

    @property
    def isPrivate(self) -> bool:
        res = self._do_request(
            "GET",
            endpoint=f"{self.endpoint}/visibility")

        if res.status_code == 404:
            raise InvalidBlob
        if res.status_code == 200:
            return res.json()["visibility"] == Visibility.PRIVATE.value

        raise BlobServiceError

    @property
    def md5(self) -> str:
        return self._hash("md5")["md5"]

    @property
    def sha256(self) -> str:
        return self._hash("sha256")["sha256"]

    def __init__(self, blobId: str, authToken: str = None):
        super().__init__(authToken)
        self.blobId = blobId

    def _hash(self, *types) -> dict[str, str]:
        if not types:
            raise ValueError("No hash types specified")

        res = self._do_request(
            "GET",
            endpoint=f"{self.endpoint}/hash",
            params={
                "type": ",".join(types)
            }
        )

        if res.status_code == 404:
            raise InvalidBlob
        if res.status_code == 200:
            return res.json()

        raise BlobServiceError

    def allowUser(self, username: str) -> None:
        res = self._do_request(
            "PATCH",
            endpoint=f"{self.endpoint}/acl",
            json={
                "acl": [
                    username
                ]
            })

        if res.status_code == 404:
            raise InvalidBlob
        if res.status_code == 204:
            return

        raise BlobServiceError

    def delete(self) -> None:
        res = self._do_request(
            "DELETE",
            endpoint=self.endpoint)

        if res.status_code == 404:
            raise InvalidBlob
        if res.status_code == 204:
            return

        raise BlobServiceError

    def dumpToFile(self, localFilename: str | os.PathLike = None) -> None:
        res = self._do_request(
            "GET",
            endpoint=self.endpoint,
            stream=True)

        if res.status_code == 404:
            raise InvalidBlob
        if res.status_code == 200:
            filename = localFilename if localFilename is not None else self.blobId
            with open(filename, "wb") as f:
                stream.stream_response_to_file(res, f, chunksize = 1024 * 1024)
            return

        raise BlobServiceError

    def revokeUser(self, username: str) -> None:
        res = self._do_request(
            "DELETE",
            endpoint=f"{self.endpoint}/acl/{username}")

        if res.status_code == 404:
            raise InvalidBlob
        if res.status_code == 204:
            return

        raise BlobServiceError

    def setVisibility(self, private: bool) -> None:
        res = self._do_request(
            "PUT",
            endpoint=f"{self.endpoint}/visibility",
            json={
                "visibility": Visibility.PRIVATE.value if private else Visibility.PUBLIC.value
            })

        if res.status_code == 404:
            raise InvalidBlob
        if res.status_code == 204:
            return

        raise BlobServiceError

    def uploadFromFile(self, localFilename: str | os.PathLike) -> None:
        with open(localFilename, "rb") as f:
            res = self._do_request(
                "PUT",
                endpoint=self.endpoint,
                data=f)

        if res.status_code == 404:
            raise InvalidBlob
        if res.status_code == 204:
            return

        raise BlobServiceError
