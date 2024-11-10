import unittest
from unittest.mock import Mock, patch

from src.entity.memo import MemoStatusEnum
from src.formatter.common import Formatter
from src.formatter.memo_formatter import AddMemoFormatterFactory


class TestAddMemoFormatterFactory(unittest.TestCase):

    def test_get_formatters(self):

        with patch(
            "src.formatter.memo_formatter.StringFormatter"
        ) as mock_string_formatter, patch(
            "src.formatter.memo_formatter.DataFormatter"
        ) as mock_data_formatter, patch(
            "src.formatter.memo_formatter.IntegerFormatter"
        ) as mock_integer_formatter, patch(
            "src.formatter.memo_formatter.CreateFieldFormatter"
        ) as mock_create_field_formatter, patch(
            "src.formatter.memo_formatter.EnumFormatter"
        ) as mock_enum_formatter:

            mock_formatters = {
                "title": Mock(spec=Formatter),
                "description": Mock(spec=Formatter),
                "due_date": Mock(spec=Formatter),
                "total_pomodoros": Mock(spec=Formatter),
                "create_now_pomodoros": Mock(spec=Formatter),
                "now_pomodoros": Mock(spec=Formatter),
                "create_status": Mock(spec=Formatter),
                "status": Mock(spec=Formatter),
            }
            mock_string_formatter.side_effect = [
                mock_formatters["title"],
                mock_formatters["description"],
            ]
            mock_data_formatter.return_value = mock_formatters["due_date"]
            mock_integer_formatter.side_effect = [
                mock_formatters["total_pomodoros"],
                mock_formatters["now_pomodoros"],
            ]
            mock_create_field_formatter.side_effect = [
                mock_formatters["create_now_pomodoros"],
                mock_formatters["create_status"],
            ]
            mock_enum_formatter.return_value = mock_formatters["status"]

            formatter_factory = AddMemoFormatterFactory()
            formatters = formatter_factory.get_formatters()

            self.assertEqual(formatters, list(mock_formatters.values()))
            mock_string_formatter.assert_any_call("title")
            mock_string_formatter.assert_any_call("description")
            mock_data_formatter.assert_called_once_with("due_date")
            mock_integer_formatter.assert_any_call("total_pomodoros")
            mock_integer_formatter.assert_any_call("now_pomodoros")
            mock_create_field_formatter.assert_any_call("now_pomodoros", 0)
            mock_create_field_formatter.assert_any_call("status", MemoStatusEnum.TODO)
            mock_enum_formatter.assert_called_once_with("status", MemoStatusEnum)


if __name__ == "__main__":
    unittest.main()
