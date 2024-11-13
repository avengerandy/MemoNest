import unittest
from unittest.mock import Mock, patch

from src.entity.memo import Memo
from src.formatter.common import FormatterError, FormatterErrorCode
from src.formatter.memo_formatter import AddMemoFormatterFactory
from src.repository.common import RepositoryError, RepositoryErrorCode
from src.repository.memo_repository import MemoRepositoryInterface
from src.service.memo_service import MemoService


class TestMemoService(unittest.TestCase):

    @patch("src.service.memo_service.AddMemoFormatterFactory")
    def test_create_memo_success(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.return_value = {"title": "formatted title"}

        mock_formatter_factory_instance = Mock(spec=AddMemoFormatterFactory)
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_repo = Mock(spec=MemoRepositoryInterface)
        mock_repo.create.return_value = 1

        mock_output = Mock()

        data = {"title": "Test Memo"}
        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.create_memo(data)

        mock_formatter_factory_instance.create.assert_called_once()
        mock_formatter.handle.assert_called_once_with(data)
        mock_repo.create.assert_called_once_with(Memo(title="formatted title"))
        mock_output.output.assert_called_once_with({"memo_id": 1})
        mock_output.error_output.assert_not_called()

    @patch("src.service.memo_service.AddMemoFormatterFactory")
    def test_create_memo_formatter_error(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.side_effect = FormatterError(
            code=FormatterErrorCode.MISSING_REQUIRED_FIELD,
            message="Missing required field",
            original_exception=None,
        )

        mock_formatter_factory_instance = Mock(spec=AddMemoFormatterFactory)
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_output = Mock()

        memo_service = MemoService(memo_repo=Mock())
        memo_service.set_output(mock_output)
        memo_service.create_memo({})

        mock_output.output.assert_not_called()
        mock_output.error_output.assert_called_once_with(
            FormatterErrorCode.MISSING_REQUIRED_FIELD.value,
            "Missing required field",
        )

    @patch("src.service.memo_service.AddMemoFormatterFactory")
    def test_create_memo_repository_error(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.side_effect = RepositoryError(
            code=RepositoryErrorCode.FAILED_TO_CREATE_MEMO,
            message="Failed to create memo",
            original_exception=None,
        )

        mock_formatter_factory_instance = Mock(spec=AddMemoFormatterFactory)
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_output = Mock()

        memo_service = MemoService(memo_repo=Mock())
        memo_service.set_output(mock_output)
        memo_service.create_memo({})

        mock_output.output.assert_not_called()
        mock_output.error_output.assert_called_once_with(
            RepositoryErrorCode.FAILED_TO_CREATE_MEMO.value,
            "Failed to create memo",
        )


if __name__ == "__main__":
    unittest.main()
