import unittest
from unittest.mock import Mock, patch

from src.formatter.common import Formatter
from src.formatter.memo_formatter import (
    AddMemoFormatterFactory,
    DeleteMemoFormatterFactory,
    GetMemoFormatterFactory,
    UpdateMemoFormatterFactory,
)


class TestAddMemoFormatterFactory(unittest.TestCase):

    @patch("src.formatter.memo_formatter.StringFormatter")
    def test_get_formatters(self, mock_string_formatter):

        mock_string_formatter_instance = Mock(spec=Formatter)
        mock_string_formatter.return_value = mock_string_formatter_instance
        formatter_factory = AddMemoFormatterFactory()
        formatters = formatter_factory.get_formatters()

        self.assertEqual(formatters, [mock_string_formatter_instance])
        mock_string_formatter.assert_any_call("title")


class TestGetMemoFormatterFactory(unittest.TestCase):

    @patch("src.formatter.memo_formatter.IntegerFormatter")
    def test_get_formatters(self, mock_integer_formatter):

        mock_integer_formatter_instance = Mock(spec=Formatter)
        mock_integer_formatter.return_value = mock_integer_formatter_instance
        formatter_factory = GetMemoFormatterFactory()
        formatters = formatter_factory.get_formatters()

        self.assertEqual(formatters, [mock_integer_formatter_instance])
        mock_integer_formatter.assert_any_call("id")


class TestUpdateMemoFormatterFactory(unittest.TestCase):

    @patch("src.formatter.memo_formatter.IntegerFormatter")
    @patch("src.formatter.memo_formatter.StringFormatter")
    def test_get_formatters(self, mock_string_formatter, mock_integer_formatter):

        mock_integer_formatter_instance = Mock(spec=Formatter)
        mock_integer_formatter.return_value = mock_integer_formatter_instance
        mock_string_formatter_instance = Mock(spec=Formatter)
        mock_string_formatter.return_value = mock_string_formatter_instance
        formatter_factory = UpdateMemoFormatterFactory()
        formatters = formatter_factory.get_formatters()

        self.assertEqual(
            formatters,
            [
                mock_integer_formatter_instance,
                mock_string_formatter_instance,
            ],
        )
        mock_integer_formatter.assert_any_call("id")
        mock_string_formatter.assert_any_call("title")


class TestDeleteMemoFormatterFactory(unittest.TestCase):

    @patch("src.formatter.memo_formatter.IntegerFormatter")
    def test_get_formatters(self, mock_integer_formatter):

        mock_integer_formatter_instance = Mock(spec=Formatter)
        mock_integer_formatter.return_value = mock_integer_formatter_instance
        formatter_factory = DeleteMemoFormatterFactory()
        formatters = formatter_factory.get_formatters()

        self.assertEqual(formatters, [mock_integer_formatter_instance])
        mock_integer_formatter.assert_any_call("id")


if __name__ == "__main__":
    unittest.main()
