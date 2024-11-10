"""A module for defining the memo formatter."""

from typing import List

from src.entity.memo import MemoStatusEnum
from src.formatter.common import (
    CreateFieldFormatter,
    DataFormatter,
    EnumFormatter,
    Formatter,
    FormatterFactory,
    IntegerFormatter,
    StringFormatter,
)


class AddMemoFormatterFactory(FormatterFactory):
    """Factory class for creating memo formatter chains."""

    def get_formatters(self) -> List[Formatter]:
        """Return a formatter chain for adding memos."""

        title_formatter = StringFormatter("title")
        description_formatter = StringFormatter("description")
        due_date_formatter = DataFormatter("due_date")
        total_pomodoros_formatter = IntegerFormatter("total_pomodoros")
        create_now_pomodoros_formatter = CreateFieldFormatter("now_pomodoros", 0)
        now_pomodoros_formatter = IntegerFormatter("now_pomodoros")
        create_status_formatter = CreateFieldFormatter("status", MemoStatusEnum.TODO)
        status_formatter = EnumFormatter("status", MemoStatusEnum)

        return [
            title_formatter,
            description_formatter,
            due_date_formatter,
            total_pomodoros_formatter,
            create_now_pomodoros_formatter,
            now_pomodoros_formatter,
            create_status_formatter,
            status_formatter,
        ]
