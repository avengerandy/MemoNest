"""A module for defining the repository interface for memo management."""

import datetime
from abc import ABC, abstractmethod
from sqlite3 import Connection
from typing import List, Optional

from src.entity.memo import Memo
from src.repository.common import RepositoryError, RepositoryErrorCode


class MemoRepositoryInterface(ABC):
    """
    An interface for memo repository operations.

    This interface defines the methods required for managing memos in a repository.
    All operations on memos are expected to return a new instance of Memo,
    as Memo is an immutable type. Each memo should maintain its creation and update timestamps.

    Note:
        All methods may raise a RepositoryError if any database operation fails.
    """

    @abstractmethod
    def create(self, memo: Memo) -> int:
        """
        Creates a new memo and returns the ID of the newly created memo.

        The create method sets the creation date,
        and the update date is initially set to the creation date.

        Raises:
            RepositoryError: If there is an error during the database operation.
        """

    @abstractmethod
    def update(self, memo: Memo) -> None:
        """
        Updates an existing memo.

        The update method should ensure that the update date is current whenever a memo is modified.

        Raises:
            RepositoryError: If there is an error during the database operation.
        """

    @abstractmethod
    def delete(self, memo: Memo) -> None:
        """
        Deletes the specified memo.

        This method does not return any value, as the operation's purpose is to remove the memo.

        Raises:
            RepositoryError: If there is an error during the database operation.
        """

    @abstractmethod
    def get(self, memo_id: int) -> Optional[Memo]:
        """
        Retrieve a memo by its ID.

        Returns None if the memo with the specified ID does not exist.

        Raises:
            RepositoryError: If there is an error during the database operation.
        """

    @abstractmethod
    def get_all(self) -> List[Memo]:
        """
        Retrieve all memos in the repository.

        Returns an empty list if no memos are found.

        Raises:
            RepositoryError: If there is an error during the database operation.
        """


class SQLiteMemoRepository(MemoRepositoryInterface):
    """An SQLite implementation of the MemoRepositoryInterface."""

    def __init__(self, connect: Connection):
        self.connect = connect

    def create(self, memo: Memo) -> int:
        create_date = datetime.datetime.now()
        update_date = create_date
        try:
            with self.connect:
                cursor = self.connect.cursor()
                cursor.execute(
                    "INSERT INTO memos (title, create_date, update_date) VALUES (?, ?, ?)",
                    (memo.title, create_date.isoformat(), update_date.isoformat()),
                )
                new_id = cursor.lastrowid
                return new_id
        except Exception as error:
            error_code = RepositoryErrorCode.FAILED_TO_CREATE_MEMO
            raise RepositoryError(
                error_code, error_code.get_message(), error
            ) from error

    def update(self, memo: Memo) -> None:
        update_date = datetime.datetime.now()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                cursor.execute(
                    "UPDATE memos SET title = ?, update_date = ? WHERE id = ?",
                    (memo.title, update_date.isoformat(), memo.id),
                )
        except Exception as error:
            error_code = RepositoryErrorCode.FAILED_TO_UPDATE_MEMO
            raise RepositoryError(
                error_code, error_code.get_message(), error
            ) from error

    def delete(self, memo: Memo) -> None:
        try:
            with self.connect:
                cursor = self.connect.cursor()
                cursor.execute("DELETE FROM memos WHERE id = ?", (memo.id,))
        except Exception as error:
            error_code = RepositoryErrorCode.FAILED_TO_DELETE_MEMO
            raise RepositoryError(
                error_code, error_code.get_message(), error
            ) from error

    def get(self, memo_id: int) -> Optional[Memo]:
        try:
            with self.connect:
                cursor = self.connect.cursor()
                cursor.execute("SELECT * FROM memos WHERE id = ?", (memo_id,))
                row = cursor.fetchone()
                if row:
                    return Memo(
                        id=row[0],
                        title=row[1],
                        create_date=datetime.datetime.fromisoformat(row[2]),
                        update_date=datetime.datetime.fromisoformat(row[3]),
                    )
                return None
        except Exception as error:
            error_code = RepositoryErrorCode.FAILED_TO_GET_MEMO
            raise RepositoryError(
                error_code, error_code.get_message(), error
            ) from error

    def get_all(self) -> List[Memo]:
        try:
            with self.connect:
                cursor = self.connect.cursor()
                cursor.execute("SELECT * FROM memos")
                rows = cursor.fetchall()
                return [
                    Memo(
                        id=row[0],
                        title=row[1],
                        create_date=datetime.datetime.fromisoformat(row[2]),
                        update_date=datetime.datetime.fromisoformat(row[3]),
                    )
                    for row in rows
                ]
        except Exception as error:
            error_code = RepositoryErrorCode.FAILED_TO_GET_ALL_MEMOS
            raise RepositoryError(
                error_code, error_code.get_message(), error
            ) from error

    def create_table_if_not_exists(self):
        """Create the memos table if it does not exist."""

        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(
                (
                    "CREATE TABLE IF NOT EXISTS memos (",
                    "id INTEGER PRIMARY KEY AUTOINCREMENT,",
                    "title TEXT NOT NULL,",
                    "create_date TEXT NOT NULL,",
                    "update_date TEXT NOT NULL",
                    ")",
                )
            )
