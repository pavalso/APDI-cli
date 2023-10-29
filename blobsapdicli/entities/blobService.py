import os

from blobsapdicli.enums import Visibility
from blobsapdicli.exceptions import InvalidBlob, Unauthorized, BlobServiceError
from blobsapdicli.entities.blob import Blob
from blobsapdicli.entities._apiRequester import _ApiRequester


class BlobService(_ApiRequester):

    def __init__(self, serviceURL: str, authToken: str = None) -> None:
        super().__init__(authToken, serviceURL)

    def createBlob(self, localFilename: str | os.PathLike) -> Blob:
        res = self._do_request(
            "POST",
            endpoint="blobs",
            json={
                "visibility": Visibility.PRIVATE.value
            }
        )

        if res.status_code == 401:
            raise Unauthorized
        if res.status_code == 201:
            blob = Blob(res.json()["blobId"], self.authToken)

            blob.uploadFromFile(localFilename)

            return blob

        raise BlobServiceError

    def deleteBlob(self, blob: Blob) -> None:
        res = self._do_request(
            "DELETE",
            endpoint=f"blobs/{blob.blobId}"
        )

        if res.status_code == 404:
            raise InvalidBlob
        if res.status_code == 204:
            return

        raise BlobServiceError

    def getBlob(self, blobId: str) -> Blob:
        res = self._do_request(
            "GET",
            endpoint=f"blobs/{blobId}"
        )

        if res.status_code == 404:
            raise InvalidBlob
        if res.status_code == 200:
            blob = Blob(blobId, self.authToken)
            return blob

        raise BlobServiceError

    def getBlobs(self) -> list[str]:
        res = self._do_request(
            "GET",
            endpoint="blobs/"
        )

        if res.status_code == 401:
            raise Unauthorized
        if res.status_code == 200:
            return [
                blob_info["blobId"]
                for blob_info
                in res.json()["blobs"]
                ]

        raise BlobServiceError
