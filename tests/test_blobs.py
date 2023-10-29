import unittest
import requests
import json

from unittest.mock import patch

from blobsapdicli import Blob, Visibility, exceptions


class TestBlobs(unittest.TestCase):

    def setUp(self) -> None:
        self.blob = Blob("123")

    @patch('requests.request')
    def test_allowed_users_404(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 404

        mock_request.return_value = response

        with self.assertRaises(exceptions.InvalidBlob):
            self.blob.allowedUsers

    @patch('requests.request')
    def test_allowed_users_200(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            "allowed_users": ["123", "456"]
        }).encode()

        mock_request.return_value = response

        self.assertEqual(self.blob.allowedUsers, ["123", "456"])

    @patch('requests.request')
    def test_allowed_users_204(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 204

        mock_request.return_value = response

        self.assertEqual(self.blob.allowedUsers, [])

    @patch('requests.request')
    def test_allowed_users_500(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 500

        mock_request.return_value = response

        with self.assertRaises(exceptions.BlobServiceError):
            self.blob.allowedUsers

    @patch('requests.request')
    def test_is_private_404(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 404

        mock_request.return_value = response

        with self.assertRaises(exceptions.InvalidBlob):
            self.blob.isPrivate

    @patch('requests.request')
    def test_is_private_200(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            "visibility": Visibility.PRIVATE.value
        }).encode()

        mock_request.return_value = response

        self.assertTrue(self.blob.isPrivate)

    @patch('requests.request')
    def test_is_private_500(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 500

        mock_request.return_value = response

        with self.assertRaises(exceptions.BlobServiceError):
            self.blob.isPrivate

    @patch('requests.request')
    def test_md5(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            "md5": "123"
        }).encode()

        mock_request.return_value = response

        self.assertEqual(self.blob.md5, "123")

    @patch('requests.request')
    def test_sha256(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            "sha256": "123"
        }).encode()

        mock_request.return_value = response

        self.assertEqual(self.blob.sha256, "123")

    @patch('requests.request')
    def test_hash_404(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 404

        mock_request.return_value = response

        with self.assertRaises(exceptions.InvalidBlob):
            self.blob._hash("md5")

    @patch('requests.request')
    def test_hash_200(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            "md5": "123"
        }).encode()

        mock_request.return_value = response

        self.assertEqual(self.blob._hash("md5"), {"md5": "123"})

    @patch('requests.request')
    def test_hash_500(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 500

        mock_request.return_value = response

        with self.assertRaises(exceptions.BlobServiceError):
            self.blob._hash("md5")

    @patch('requests.request')
    def test_allow_user_204(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 204

        mock_request.return_value = response

        self.blob.allowUser("123")

    @patch('requests.request')
    def test_allow_user_404(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 404

        mock_request.return_value = response

        with self.assertRaises(exceptions.InvalidBlob):
            self.blob.allowUser("123")

    @patch('requests.request')
    def test_allow_user_500(self, mock_request) -> None:
        response = requests.Response()

        response.status_code = 500

        mock_request.return_value = response

        with self.assertRaises(exceptions.BlobServiceError):
            self.blob.allowUser("123")
