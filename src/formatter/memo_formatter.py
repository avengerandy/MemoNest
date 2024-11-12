"""A module for defining the memo formatter."""

from typing import List

from src.formatter.common import Formatter, FormatterFactory, StringFormatter


class AddMemoFormatterFactory(FormatterFactory):
    """Factory class for creating memo formatter chains."""

    def get_formatters(self) -> List[Formatter]:
        """Return a formatter chain for adding memos."""

        title_formatter = StringFormatter("title")

        return [title_formatter]
