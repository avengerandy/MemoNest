"""This module defines the Memo and MemoStatusEnum classes."""

import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class MemoStatusEnum(Enum):
    """Enumeration for memo status."""

    TODO = "todo"
    DOING = "doing"
    DONE = "done"


@dataclass(frozen=True)
class Memo:
    """
    An immutable memo entity.

    Attributes:
        title (str): The title of the memo.
        description (str): A brief description of the memo.
        due_date (datetime): The due date for the memo.
        total_pomodoros (int): Total number of pomodoros planned for the memo.
        now_pomodoros (int): Number of pomodoros completed so far.
        status (MemoStatusEnum): The current status of the memo.
        create_date (Optional[datetime]): The creation date of the memo.
        update_date (Optional[datetime]): The last update date of the memo.
        id (Optional[int]): The unique identifier for the memo.
    """

    title: str
    description: str
    due_date: datetime.datetime
    total_pomodoros: int
    now_pomodoros: int
    status: MemoStatusEnum
    create_date: Optional[datetime.datetime] = None
    update_date: Optional[datetime.datetime] = None
    id: Optional[int] = None

    def is_create(self) -> bool:
        """Check if the memo has been created."""
        return self.id is not None
