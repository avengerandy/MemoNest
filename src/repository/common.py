"""A module for defining the repository common class."""

from enum import Enum


class RepositoryErrorCode(Enum):
    """Custom exception code for repository-related errors."""

    FAILED_TO_CREATE_MEMO = 101
    FAILED_TO_UPDATE_MEMO = 102
    FAILED_TO_DELETE_MEMO = 103
    FAILED_TO_GET_MEMO = 104
    FAILED_TO_GET_ALL_MEMOS = 105

    def get_message(self) -> str:
        """Return a human-readable message for the error code."""
        return self.name.lower().capitalize().replace("_", " ")


class RepositoryError(Exception):
    """Custom exception for repository-related errors."""

    def __init__(
        self, code: RepositoryErrorCode, message: str, original_exception: Exception
    ):
        super().__init__(message)
        self.code = code
        self.original_exception = original_exception
