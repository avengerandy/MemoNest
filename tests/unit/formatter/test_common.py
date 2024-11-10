import unittest
from typing import List
from unittest.mock import Mock

from src.formatter.common import (
    Formatter,
    FormatterError,
    FormatterErrorCode,
    FormatterFactory,
    FormatterHelper,
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


class TestFormatterFactoryTests(unittest.TestCase):

    def test_create(self):
        formatter1 = Mock(spec=Formatter)
        formatter2 = Mock(spec=Formatter)
        formatter3 = Mock(spec=Formatter)

        class TestFormatterFactory(FormatterFactory):
            def get_formatters(self) -> List[Formatter]:
                return [formatter1, formatter2, formatter3]

        test_formatter_factory = TestFormatterFactory()
        formatter = test_formatter_factory.create()

        self.assertEqual(formatter, formatter1)
        formatter1.set_next.assert_called_once_with(formatter2)
        formatter2.set_next.assert_called_once_with(formatter3)
        self.assertFalse(formatter3.set_next.called)


if __name__ == "__main__":
    unittest.main()
