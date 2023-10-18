import os

import requests

from adiauthcli import Client


class Blob:

    url = os.getenv("BLOB_URL", "http://localhost:3002")

    __api_version__ = "v1"

    def __init__(self) -> None:
        pass

    def create(self, data, token) -> str:
        res = requests.post(
            f"{self.url}/api/{Blob.__api_version__}/blobs",
            headers={"Authorization": f"{token}"},
            json=data)

        if res.status_code == 201:
            return res.json()["id"]

        if res.status_code == 401:
            raise Exception(res.json()["error"])

        raise Exception(res.json()["error"])

    def fetch(self, blob_id, token) -> str:
        res = requests.get(
            f"{self.url}/api/{Blob.__api_version__}/blobs/{blob_id}",
            headers={"Authorization": f"{token}"})

        if res.status_code == 200:
            return res.text

        if res.status_code == 404:
            raise Exception(res.json()["error"])

        if res.status_code == 401:
            raise Exception(res.json()["error"])

        raise Exception(res.json()["error"])

if __name__ == "__main__":
    client = Client("http://localhost:3001/")
    client.login("test", "test")

    blob = Blob()
    id = blob.create({
        "visibility": 0
    }, client._token_)
    print(blob.fetch(id, client._token_))
