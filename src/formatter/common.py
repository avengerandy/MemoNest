"""A module for defining the formatter common class."""

import re
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional


class FormatterErrorCode(Enum):
    """Custom exception code for formatter-related errors."""

    MISSING_REQUIRED_FIELD = 1
    INVALID_FIELD_FORMAT = 2
    INVALID_FIELD_VALUE = 3

    def get_message(self) -> str:
        """Return a human-readable message for the error code."""

        return self.name.lower().capitalize().replace("_", " ")


class FormatterError(Exception):
    """Custom exception for formatter-related errors."""

    def __init__(
        self,
        code: FormatterErrorCode,
        message: str,
        original_exception: Optional[Exception],
    ):
        super().__init__(message)
        self.code = code
        self.original_exception = original_exception


class FormatterHelper:
    """A helper class for formatter-related operations."""

    @staticmethod
    def validate_field_exist(data: dict, field_name: str) -> None:
        """Validate if a field is present in the data."""

        if field_name not in data:
            error_code = FormatterErrorCode.MISSING_REQUIRED_FIELD
            FormatterHelper.raise_field_error(field_name, error_code)

    @staticmethod
    def validate_field_format_with_regex(
        data: dict, field_name: str, format_regex: str
    ) -> None:
        """Validate if a field has the correct format."""

        field_value = data[field_name]
        if not re.match(format_regex, field_value):
            error_code = FormatterErrorCode.INVALID_FIELD_FORMAT
            FormatterHelper.raise_field_error(field_name, error_code)

    @staticmethod
    def raise_field_error(
        field_name: str,
        error_code: FormatterErrorCode,
        error: Optional[Exception] = None,
    ) -> None:
        """Raise an error for a field."""

        error_message = f"Error in field [{field_name}]: {error_code.get_message()}."
        raise FormatterError(error_code, error_message, error) from error


class Formatter(ABC):
    """An abstract class for defining a formatter."""

    def __init__(self):
        self._next_formatter = None

    def handle(self, data: dict) -> dict:
        """Handle the data with the format method and pass it to the next formatter in the chain."""

        formatted_data = self.format(data)
        if self._next_formatter:
            return self._next_formatter.handle(formatted_data)
        return formatted_data

    @abstractmethod
    def format(self, data: dict) -> dict:
        """Format the data."""

    def set_next(self, next_formatter: "Formatter") -> None:
        """Set the next formatter in the chain."""

        self._next_formatter = next_formatter


class DateFormatter(Formatter):
    """A Formatter class for converting a field value to a date."""

    DATE_REGEX = r"\d{4}-\d{2}-\d{2}"
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, field_name):
        super().__init__()
        self.field_name = field_name

    def format(self, data) -> dict:
        """Convert a field value to a date."""

        FormatterHelper.validate_field_exist(data, self.field_name)
        FormatterHelper.validate_field_format_with_regex(
            data, self.field_name, DateFormatter.DATE_REGEX
        )

        try:
            data[self.field_name] = datetime.strptime(
                data[self.field_name], DateFormatter.DATE_FORMAT
            ).date()
        except (ValueError, TypeError) as error:
            error_code = FormatterErrorCode.INVALID_FIELD_VALUE
            FormatterHelper.raise_field_error(self.field_name, error_code, error)

        return data


class IntegerFormatter(Formatter):
    """A Formatter class for converting a field value to an integer."""

    INT_REGEX = r"\d+"

    def __init__(self, field_name):
        super().__init__()
        self.field_name = field_name

    def format(self, data) -> dict:
        """Convert a field value to an integer."""

        FormatterHelper.validate_field_exist(data, self.field_name)
        FormatterHelper.validate_field_format_with_regex(
            data, self.field_name, IntegerFormatter.INT_REGEX
        )

        try:
            data[self.field_name] = int(data[self.field_name])
        except (ValueError, TypeError) as error:
            error_code = FormatterErrorCode.INVALID_FIELD_VALUE
            FormatterHelper.raise_field_error(self.field_name, error_code, error)

        return data


class StringFormatter(Formatter):
    """A Formatter class for converting a field value to a string."""

    def __init__(self, field_name):
        super().__init__()
        self.field_name = field_name

    def format(self, data) -> dict:
        """Convert a field value to a string."""

        FormatterHelper.validate_field_exist(data, self.field_name)

        try:
            data[self.field_name] = str(data[self.field_name])
        except (ValueError, TypeError, AttributeError) as error:
            error_code = FormatterErrorCode.INVALID_FIELD_VALUE
            FormatterHelper.raise_field_error(self.field_name, error_code, error)

        return data


class EnumFormatter(Formatter):
    """A Formatter class for converting a field value to an enum value."""

    def __init__(self, field_name, enum_class):
        super().__init__()
        self.field_name = field_name
        self.enum_class = enum_class

    def format(self, data) -> dict:
        """Convert a field value to an enum value."""

        FormatterHelper.validate_field_exist(data, self.field_name)

        try:
            data[self.field_name] = self.enum_class(data[self.field_name])
        except (ValueError, TypeError) as error:
            error_code = FormatterErrorCode.INVALID_FIELD_VALUE
            FormatterHelper.raise_field_error(self.field_name, error_code, error)

        return data


class CreateFieldFormatter(Formatter):
    """A Formatter class for creating a field with a default value if it is missing."""

    def __init__(self, field_name, field_value):
        super().__init__()
        self.field_name = field_name
        self.field_value = field_value

    def format(self, data) -> dict:
        """Create a default value for a field if it is missing."""

        if self.field_name not in data:
            data[self.field_name] = self.field_value

        return data


class FormatterFactory(ABC):
    """An abstract Factory class for creating formatter chains."""

    @abstractmethod
    def get_formatters(self) -> List[Formatter]:
        """Return a list of ordered formatters."""

    def create(self) -> Formatter:
        """Set the next formatter in the chain for a list of formatters."""

        formatters = self.get_formatters()
        for i in range(len(formatters) - 1):
            formatters[i].set_next(formatters[i + 1])

        return formatters[0]
