import unittest
from unittest.mock import Mock, patch

from src.formatter.common import Formatter
from src.formatter.memo_formatter import AddMemoFormatterFactory


class TestAddMemoFormatterFactory(unittest.TestCase):

    @patch("src.formatter.memo_formatter.StringFormatter")
    def test_get_formatters(self, mock_string_formatter):

        mock_string_formatter_instance = Mock(spec=Formatter)
        mock_string_formatter.return_value = mock_string_formatter_instance
        formatter_factory = AddMemoFormatterFactory()
        formatters = formatter_factory.get_formatters()

        self.assertEqual(formatters, [mock_string_formatter_instance])
        mock_string_formatter.assert_any_call("title")


if __name__ == "__main__":
    unittest.main()
