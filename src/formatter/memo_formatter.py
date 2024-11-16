"""A module for defining the memo formatter."""

from typing import List

from src.formatter.common import (
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

        return [title_formatter]


class GetMemoFormatterFactory(FormatterFactory):
    """Factory class for get memo formatter chains."""

    def get_formatters(self) -> List[Formatter]:
        """Return a formatter chain for getting memos."""

        id_formatter = IntegerFormatter("id")

        return [id_formatter]


class UpdateMemoFormatterFactory(FormatterFactory):
    """Factory class for updating memo formatter chains."""

    def get_formatters(self) -> List[Formatter]:
        """Return a formatter chain for updating memos."""

        id_formatter = IntegerFormatter("id")
        title_formatter = StringFormatter("title")

        return [id_formatter, title_formatter]


class DeleteMemoFormatterFactory(FormatterFactory):
    """Factory class for deleting memo formatter chains."""

    def get_formatters(self) -> List[Formatter]:
        """Return a formatter chain for deleting memos."""

        id_formatter = IntegerFormatter("id")

        return [id_formatter]
