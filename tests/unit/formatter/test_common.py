import datetime
import unittest
from enum import Enum
from typing import List
from unittest.mock import MagicMock, Mock, patch

from src.formatter.common import (
    CreateFieldFormatter,
    DateFormatter,
    EnumFormatter,
    Formatter,
    FormatterError,
    FormatterErrorCode,
    FormatterFactory,
    FormatterHelper,
    IntegerFormatter,
    StringFormatter,
)


class TestFormatterErrorCode(unittest.TestCase):

    def test_enum_values(self):
        self.assertEqual(FormatterErrorCode.MISSING_REQUIRED_FIELD.value, 1)
        self.assertEqual(FormatterErrorCode.INVALID_FIELD_FORMAT.value, 2)
        self.assertEqual(FormatterErrorCode.INVALID_FIELD_VALUE.value, 3)

    def test_get_message(self):
        for code in FormatterErrorCode:
            expected_message = code.name.lower().replace("_", " ").capitalize()
            self.assertEqual(code.get_message(), expected_message)

    def test_invalid_enum_value(self):
        invalid_status = 999
        with self.assertRaises(ValueError):
            FormatterErrorCode(invalid_status)


class TestFormatterError(unittest.TestCase):

    def test_initialization(self):
        original_exception = Exception("Original exception")
        error_code = FormatterErrorCode.MISSING_REQUIRED_FIELD
        error_message = error_code.get_message()

        format_error = FormatterError(error_code, error_message, original_exception)

        self.assertEqual(format_error.code, error_code)
        self.assertEqual(str(format_error), error_message)
        self.assertEqual(format_error.original_exception, original_exception)


class TestFormatterHelper(unittest.TestCase):

    def test_validate_field_exist(self):
        data = {"existing_field": "value"}

        FormatterHelper.validate_field_exist(data, "existing_field")

        with self.assertRaises(FormatterError) as context:
            FormatterHelper.validate_field_exist(data, "missing_field")

        self.assertEqual(
            context.exception.code, FormatterErrorCode.MISSING_REQUIRED_FIELD
        )

    def test_validate_field_format_with_regex(self):
        data = {"field": "123"}
        regex = r"\d+"

        FormatterHelper.validate_field_format_with_regex(data, "field", regex)

        data["field"] = "abc"
        with self.assertRaises(FormatterError) as context:
            FormatterHelper.validate_field_format_with_regex(data, "field", regex)

        self.assertEqual(
            context.exception.code, FormatterErrorCode.INVALID_FIELD_FORMAT
        )

    def test_raise_field_error(self):
        with self.assertRaises(FormatterError) as context:
            FormatterHelper.raise_field_error(
                "test_field", FormatterErrorCode.MISSING_REQUIRED_FIELD
            )

        self.assertEqual(
            context.exception.code, FormatterErrorCode.MISSING_REQUIRED_FIELD
        )
        self.assertIn(
            "Error in field [test_field]: Missing required field.",
            str(context.exception),
        )


class TestFormatter(unittest.TestCase):

    def test_set_next_and_handle(self):
        class EmptyFormatter(Formatter):
            def format(self, data: dict) -> dict:
                return data

        class HandledFormatter(Formatter):
            def format(self, data: dict) -> dict:
                data["handled"] = True
                return data

        empty_formatter = EmptyFormatter()
        handled_formatter = HandledFormatter()
        empty_formatter.set_next(handled_formatter)

        result = empty_formatter.handle({})

        self.assertTrue(result["handled"])


class TestDateFormatter(unittest.TestCase):

    @patch("src.formatter.common.FormatterHelper")
    def test_format(self, mock_formatter_helper):
        data = {"date_field": "2021-01-01"}
        date_formatter = DateFormatter("date_field")

        result = date_formatter.format(data)

        self.assertEqual(
            result["date_field"],
            datetime.date(2021, 1, 1),
        )
        mock_formatter_helper.validate_field_exist.assert_called_once_with(
            data, "date_field"
        )
        mock_formatter_helper.validate_field_format_with_regex.assert_called_once_with(
            data,
            "date_field",
            DateFormatter.DATE_REGEX,
        )

    @patch("src.formatter.common.FormatterHelper")
    @patch("src.formatter.common.datetime")
    def test_format_invalid_field_value(self, mock_datetime, mock_formatter_helper):
        data = {"date_field": "not_a_date"}
        date_formatter = DateFormatter("date_field")
        mock_datetime.strptime.side_effect = ValueError("Invalid date format")

        date_formatter.format(data)

        mock_datetime.strptime.assert_called_once_with(
            "not_a_date",
            DateFormatter.DATE_FORMAT,
        )
        mock_formatter_helper.raise_field_error.assert_called_once()
        args = mock_formatter_helper.raise_field_error.call_args[0]
        self.assertEqual(args[0], "date_field")
        self.assertEqual(args[1], FormatterErrorCode.INVALID_FIELD_VALUE)
        self.assertIsInstance(args[2], ValueError)


class TestIntegerFormatter(unittest.TestCase):

    @patch("src.formatter.common.FormatterHelper")
    def test_format(self, mock_formatter_helper):
        data = {"integer_field": "123"}
        integer_formatter = IntegerFormatter("integer_field")

        result = integer_formatter.format(data)

        self.assertEqual(result["integer_field"], 123)
        mock_formatter_helper.validate_field_exist.assert_called_once_with(
            data, "integer_field"
        )
        mock_formatter_helper.validate_field_format_with_regex.assert_called_once_with(
            data,
            "integer_field",
            IntegerFormatter.INT_REGEX,
        )

    @patch("src.formatter.common.FormatterHelper")
    def test_format_invalid_field_value(self, mock_formatter_helper):
        data = {"integer_field": "not_an_integer"}
        integer_formatter = IntegerFormatter("integer_field")

        integer_formatter.format(data)

        mock_formatter_helper.raise_field_error.assert_called_once()
        args = mock_formatter_helper.raise_field_error.call_args[0]
        self.assertEqual(args[0], "integer_field")
        self.assertEqual(args[1], FormatterErrorCode.INVALID_FIELD_VALUE)
        self.assertIsInstance(args[2], ValueError)


class TestStringFormatter(unittest.TestCase):

    @patch("src.formatter.common.FormatterHelper")
    def test_format(self, mock_formatter_helper):
        data = {"string_field": 123}
        string_formatter = StringFormatter("string_field")

        result = string_formatter.format(data)

        self.assertEqual(result["string_field"], "123")
        mock_formatter_helper.validate_field_exist.assert_called_once_with(
            data, "string_field"
        )

    @patch("src.formatter.common.FormatterHelper")
    def test_format_invalid_field_value(self, mock_formatter_helper):
        object_without_str = MagicMock()
        object_without_str.__str__.side_effect = ValueError()
        data = {"string_field": object_without_str}
        string_formatter = StringFormatter("string_field")

        string_formatter.format(data)

        mock_formatter_helper.raise_field_error.assert_called_once()
        args = mock_formatter_helper.raise_field_error.call_args[0]
        self.assertEqual(args[0], "string_field")
        self.assertEqual(args[1], FormatterErrorCode.INVALID_FIELD_VALUE)


class TestEnumFormatter(unittest.TestCase):

    @patch("src.formatter.common.FormatterHelper")
    def test_format(self, mock_formatter_helper):
        class TestEnum(Enum):
            VALUE1 = "value1"
            VALUE2 = "value2"

        data = {"enum_field": "value1"}
        enum_formatter = EnumFormatter("enum_field", TestEnum)

        result = enum_formatter.format(data)

        self.assertEqual(result["enum_field"], TestEnum.VALUE1)
        mock_formatter_helper.validate_field_exist.assert_called_once_with(
            data, "enum_field"
        )

    @patch("src.formatter.common.FormatterHelper")
    def test_format_invalid_field_value(self, mock_formatter_helper):
        class TestEnum(Enum):
            VALUE1 = "value1"
            VALUE2 = "value2"

        data = {"enum_field": "invalid_value"}
        enum_formatter = EnumFormatter("enum_field", TestEnum)

        enum_formatter.format(data)

        mock_formatter_helper.raise_field_error.assert_called_once()
        args = mock_formatter_helper.raise_field_error.call_args[0]
        self.assertEqual(args[0], "enum_field")
        self.assertEqual(args[1], FormatterErrorCode.INVALID_FIELD_VALUE)


class TestCreateFieldFormatter(unittest.TestCase):

    def test_format(self):
        data = {}
        field_name = "new_field"
        field_value = "default_value"
        create_field_formatter = CreateFieldFormatter(field_name, field_value)

        result = create_field_formatter.format(data)

        self.assertEqual(result[field_name], field_value)


class TestFormatterFactory(unittest.TestCase):

    def test_create(self):
        formatter1 = Mock(spec=Formatter)
        formatter2 = Mock(spec=Formatter)
        formatter3 = Mock(spec=Formatter)

        class TestFormatterFactorySubClass(FormatterFactory):
            def get_formatters(self) -> List[Formatter]:
                return [formatter1, formatter2, formatter3]

        test_formatter_factory = TestFormatterFactorySubClass()
        formatter = test_formatter_factory.create()

        self.assertEqual(formatter, formatter1)
        formatter1.set_next.assert_called_once_with(formatter2)
        formatter2.set_next.assert_called_once_with(formatter3)
        self.assertFalse(formatter3.set_next.called)


if __name__ == "__main__":
    unittest.main()
