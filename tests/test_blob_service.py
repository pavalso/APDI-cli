import unittest
import requests
import json

from unittest.mock import patch

from blobsapdicli import Blob, BlobService, exceptions


class TestBlobService(unittest.TestCase):

    def setUp(self) -> None:
        self.blob_service = BlobService("http://test.com")

    @patch('requests.request')
    def test_create_401(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 401

        mock_request.return_value = response

        with self.assertRaises(exceptions.Unauthorized):
            self.blob_service.createBlob("tests/test_file.txt")

    @patch('requests.request')
    @patch('blobsapdicli.entities.blobService.Blob.uploadFromFile')
    def test_create_201(self, mock_uploadFromFile, mock_request) -> None:
        response = requests.Response()

        response.status_code = 201
        response._content = json.dumps({
            "blobId": "123",
            "URL": "https://127.0.0.1/123"
        }).encode()

        mock_request.return_value = response

        mock_uploadFromFile.return_value = Blob("123")

        self.blob_service.createBlob("tests/test_file.txt")

    @patch('requests.request')
    def test_create_500(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 500

        mock_request.return_value = response

        with self.assertRaises(exceptions.BlobServiceError):
            self.blob_service.createBlob("tests/test_file.txt")

    @patch('requests.request')
    def test_delete_404(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 404

        mock_request.return_value = response

        with self.assertRaises(exceptions.InvalidBlob):
            self.blob_service.deleteBlob(Blob("123"))

    @patch('requests.request')
    def test_delete_204(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 204

        mock_request.return_value = response

        self.blob_service.deleteBlob(Blob("123"))

    @patch('requests.request')
    def test_delete_500(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 500

        mock_request.return_value = response

        with self.assertRaises(exceptions.BlobServiceError):
            self.blob_service.deleteBlob(Blob("123"))

    @patch('requests.request')
    def test_get_404(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 404

        mock_request.return_value = response

        with self.assertRaises(exceptions.InvalidBlob):
            self.blob_service.getBlob("123")

    @patch('requests.request')
    def test_get_200(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 200

        mock_request.return_value = response

        self.blob_service.getBlob("123")

    @patch('requests.request')
    def test_get_500(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 500

        mock_request.return_value = response

        with self.assertRaises(exceptions.BlobServiceError):
            self.blob_service.getBlob("123")

    @patch('requests.request')
    def test_get_all_401(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 401

        mock_request.return_value = response

        with self.assertRaises(exceptions.Unauthorized):
            self.blob_service.getBlobs()

    @patch('requests.request')
    def test_get_all_200(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            "blobs": [
                {
                    "blobId": "123",
                    "URL": "https://localhost/123"
                },
                {
                    "blobId": "456",
                    "URL": "https://localhost/456"
                }
            ]
        }).encode()

        mock_request.return_value = response

        self.assertEqual(
            self.blob_service.getBlobs(),
            ["123", "456"]
        )

    @patch('requests.request')
    def test_get_all_500(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 500

        mock_request.return_value = response

        with self.assertRaises(exceptions.BlobServiceError):
            self.blob_service.getBlobs()
