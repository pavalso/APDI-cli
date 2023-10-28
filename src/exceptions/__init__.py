"""
This module contains custom exceptions that can be raised in the application.
"""

from adiauthcli import errors as adiauth


class InvalidBlob(Exception):
    """
    Exception raised when the user attempts to perform an action on a blob that does not exist.
    """

class Unauthorized(Exception):
    """
    Exception raised when the user attempts to perform an action that they are not authorized to.
    """

class BlobServiceError(Exception):
    """
    Exception raised when an error occurs in the blob service.
    """

__all__ = ["InvalidBlob", "Unauthorized", "BlobServiceError", "adiauth"]
