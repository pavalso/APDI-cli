import io

from src.exceptions import InvalidTokenError, UnknownError

from ._blob import _Blob


class _UserBlob(_Blob):

    def __init__(self, id_: str, user_token: str) -> None:
        super().__init__(id_)
        self._token_ = user_token

    def upload(self, content: io.BufferedReader) -> None:
        res = self._do_request(
            "PUT",
            endpoint=f"{self._endpoint_}",
            data=content)

        if res.status_code == 401:
            raise InvalidTokenError
        if res.status_code == 204:
            return

        raise UnknownError(res.content)

    def delete(self) -> None:
        res = self._do_request(
            "DELETE",
            endpoint=f"{self._endpoint_}")

        if res.status_code == 401:
            raise InvalidTokenError
        if res.status_code == 204:
            return

        raise UnknownError(res.content)

__export__ = {_UserBlob}
