import os

from requests_toolbelt.downloadutils import stream

from src.exceptions import InvalidTokenError, UnknownError, BlobNotFoundError

from ._api_requester import _ApiRequester


class _Blob(_ApiRequester):

    _token_: str | None = None

    @property
    def md5(self) -> str:
        return self._hash("md5")["md5"]

    @property
    def sha256(self) -> str:
        return self._hash("sha256")["sha256"]

    @property
    def exists(self) -> bool:
        res = self._do_request(
            "HEAD",
            endpoint=f"{self._endpoint_}")

        if res.status_code == 200:
            return True
        if res.status_code == 404:
            return False

        raise UnknownError(res.content)

    def __init__(self, id_: str) -> None:
        self.id_ = id_
        self._endpoint_ = f"blobs/{self.id_}"

    def _hash(self, *types) -> dict[str, str]:
        if not types:
            raise ValueError("No hash types provided")

        res = self._do_request(
            "GET",
            endpoint=f"{self._endpoint_}/hash?type={",".join(types)}")

        if res.status_code == 401:
            raise InvalidTokenError
        if res.status_code == 200:
            return res.json()

        raise UnknownError(res.content)

    def download(self, path: os.PathLike | str = None) -> os.PathLike:
        res = self._do_request(
            "GET",
            endpoint=f"{self._endpoint_}",
            stream=True
        )

        _path = path if path is not None else os.path.join(os.getcwd(), self.id_)

        if res.status_code == 404:
            raise BlobNotFoundError(self.id_)
        if res.status_code == 200:
            return stream.stream_response_to_file(res, _path, chunksize=1024 * 1024)

        raise UnknownError(res.content)

__export__ = {_Blob}
