"""This module defines the Memo and MemoStatusEnum classes."""

import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Memo:
    """
    An immutable memo entity.

    Attributes:
        title (str): The title of the memo.
        create_date (Optional[datetime]): The creation date of the memo.
        update_date (Optional[datetime]): The last update date of the memo.
        id (Optional[int]): The unique identifier for the memo.
    """

    title: str
    create_date: Optional[datetime.datetime] = None
    update_date: Optional[datetime.datetime] = None
    id: Optional[int] = None

    def is_create(self) -> bool:
        """Check if the memo has been created."""
        return self.id is not None
