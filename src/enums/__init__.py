"""
This module defines the Perms class and the Visibility enumeration.
"""

from enum import Enum


class Visibility(str, Enum):
    """
    An enumeration representing the visibility of a permission.
    """
    PUBLIC = "public"
    PRIVATE = "private"

    def __str__(self) -> str:
        return self.name.lower()

    def __repr__(self) -> str:
        return self.__str__()
