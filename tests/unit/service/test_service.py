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
        return_memo = Memo(title="return_memo title")
        mock_repo.get.return_value = return_memo

        mock_output = Mock()

        data = {"title": "Test Memo"}
        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.create_memo(data)

        mock_formatter_factory_instance.create.assert_called_once()
        mock_formatter.handle.assert_called_once_with(data)
        mock_repo.create.assert_called_once()
        args = mock_repo.create.call_args[0]
        self.assertEqual(args[0].title, "formatted title")
        mock_repo.get.assert_called_once_with(1)
        mock_output.output.assert_called_once_with({"memo": return_memo.to_dict()})
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
        mock_formatter.handle.return_value = {"title": "formatted title"}

        mock_formatter_factory_instance = Mock(spec=AddMemoFormatterFactory)
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_repo = Mock(spec=MemoRepositoryInterface)
        mock_repo.create.side_effect = RepositoryError(
            code=RepositoryErrorCode.FAILED_TO_CREATE_MEMO,
            message="Failed to create memo",
            original_exception=None,
        )

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.create_memo({"title": "Test Memo"})

        mock_output.output.assert_not_called()
        mock_output.error_output.assert_called_once_with(
            RepositoryErrorCode.FAILED_TO_CREATE_MEMO.value,
            "Failed to create memo",
        )

    @patch("src.service.memo_service.GetMemoFormatterFactory")
    def test_get_memo_success(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.return_value = {"id": 1}

        mock_formatter_factory_instance = Mock()
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_repo = Mock(spec=MemoRepositoryInterface)
        return_memo = Memo(title="return_memo title")
        mock_repo.get.return_value = return_memo

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.get_memo({"id": 1})

        mock_formatter_factory_instance.create.assert_called_once()
        mock_formatter.handle.assert_called_once_with({"id": 1})
        mock_repo.get.assert_called_once_with(1)
        mock_output.output.assert_called_once_with({"memo": return_memo.to_dict()})
        mock_output.error_output.assert_not_called()

    @patch("src.service.memo_service.GetMemoFormatterFactory")
    def test_get_memo_formatter_error(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.side_effect = FormatterError(
            code=FormatterErrorCode.MISSING_REQUIRED_FIELD,
            message="Missing required field",
            original_exception=None,
        )

        mock_formatter_factory_instance = Mock()
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_output = Mock()

        memo_service = MemoService(memo_repo=Mock())
        memo_service.set_output(mock_output)
        memo_service.get_memo({"id": 1})

        mock_output.output.assert_not_called()
        mock_output.error_output.assert_called_once_with(
            FormatterErrorCode.MISSING_REQUIRED_FIELD.value,
            "Missing required field",
        )

    @patch("src.service.memo_service.GetMemoFormatterFactory")
    def test_get_memo_repository_error(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.return_value = {"id": 1}

        mock_formatter_factory_instance = Mock()
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_repo = Mock(spec=MemoRepositoryInterface)
        mock_repo.get.side_effect = RepositoryError(
            code=RepositoryErrorCode.FAILED_TO_GET_MEMO,
            message="Failed to get memo",
            original_exception=None,
        )

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.get_memo({"id": 1})

        mock_output.output.assert_not_called()
        mock_output.error_output.assert_called_once_with(
            RepositoryErrorCode.FAILED_TO_GET_MEMO.value,
            "Failed to get memo",
        )

    @patch("src.service.memo_service.GetMemoFormatterFactory")
    def test_get_memo_not_found(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.return_value = {"id": 1}

        mock_formatter_factory_instance = Mock()
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_repo = Mock(spec=MemoRepositoryInterface)
        mock_repo.get.return_value = None

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.get_memo({"id": 1})

        mock_output.output.assert_called_once_with({})
        mock_output.error_output.assert_not_called()

    def test_get_memos_success(self):
        mock_repo = Mock(spec=MemoRepositoryInterface)
        return_memos = [
            Memo(title="return_memo title 1"),
            Memo(title="return_memo title 2"),
        ]
        mock_repo.get_all.return_value = return_memos

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.get_memos()

        mock_repo.get_all.assert_called_once()
        memos = [memo.to_dict() for memo in return_memos]
        mock_output.output.assert_called_once_with({"list": memos})
        mock_output.error_output.assert_not_called()

    def test_get_memos_repository_error(self):
        mock_repo = Mock(spec=MemoRepositoryInterface)
        mock_repo.get_all.side_effect = RepositoryError(
            code=RepositoryErrorCode.FAILED_TO_GET_ALL_MEMOS,
            message="Failed to get all memos",
            original_exception=None,
        )

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.get_memos()

        mock_output.output.assert_not_called()
        mock_output.error_output.assert_called_once_with(
            RepositoryErrorCode.FAILED_TO_GET_ALL_MEMOS.value,
            "Failed to get all memos",
        )

    @patch("src.service.memo_service.UpdateMemoFormatterFactory")
    def test_update_memo_success(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.return_value = {"id": 1, "title": "formatted title"}

        mock_formatter_factory_instance = Mock()
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_repo = Mock(spec=MemoRepositoryInterface)
        return_memo = Memo(id=1, title="return_memo title")
        mock_repo.get.return_value = return_memo

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.update_memo({"id": 1, "title": "Test Memo"})

        mock_formatter_factory_instance.create.assert_called_once()
        mock_formatter.handle.assert_called_once_with({"id": 1, "title": "Test Memo"})
        mock_repo.update.assert_called_once()
        args = mock_repo.update.call_args[0]
        self.assertEqual(args[0].id, 1)
        self.assertEqual(args[0].title, "formatted title")
        mock_repo.get.assert_called_once_with(1)
        mock_output.output.assert_called_once_with({"memo": return_memo.to_dict()})
        mock_output.error_output.assert_not_called()

    @patch("src.service.memo_service.UpdateMemoFormatterFactory")
    def test_update_memo_formatter_error(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.side_effect = FormatterError(
            code=FormatterErrorCode.MISSING_REQUIRED_FIELD,
            message="Missing required field",
            original_exception=None,
        )

        mock_formatter_factory_instance = Mock()
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_output = Mock()

        memo_service = MemoService(memo_repo=Mock())
        memo_service.set_output(mock_output)
        memo_service.update_memo({"id": 1, "title": "Test Memo"})

        mock_output.output.assert_not_called()
        mock_output.error_output.assert_called_once_with(
            FormatterErrorCode.MISSING_REQUIRED_FIELD.value,
            "Missing required field",
        )

    @patch("src.service.memo_service.UpdateMemoFormatterFactory")
    def test_update_memo_repository_error(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.return_value = {"id": 1, "title": "formatted title"}

        mock_formatter_factory_instance = mock_formatter
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_repo = Mock(spec=MemoRepositoryInterface)
        mock_repo.update.side_effect = RepositoryError(
            code=RepositoryErrorCode.FAILED_TO_UPDATE_MEMO,
            message="Failed to update memo",
            original_exception=None,
        )

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.update_memo({})

        mock_output.output.assert_not_called()
        mock_output.error_output.assert_called_once_with(
            RepositoryErrorCode.FAILED_TO_UPDATE_MEMO.value,
            "Failed to update memo",
        )

    @patch("src.service.memo_service.UpdateMemoFormatterFactory")
    def test_update_memo_not_found(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.return_value = {"id": 1, "title": "formatted title"}

        mock_formatter_factory_instance = Mock()
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_repo = Mock(spec=MemoRepositoryInterface)
        mock_repo.get.return_value = None

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.update_memo({"id": 1, "title": "Test Memo"})

        mock_output.output.assert_called_once_with({})
        mock_output.error_output.assert_not_called()

    @patch("src.service.memo_service.DeleteMemoFormatterFactory")
    def test_delete_memo_success(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.return_value = {"id": 1}

        mock_formatter_factory_instance = Mock()
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_repo = Mock(spec=MemoRepositoryInterface)
        return_memo = Memo(id=1, title="return_memo title")
        mock_repo.get.return_value = return_memo

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.delete_memo({"id": 1})

        mock_formatter_factory_instance.create.assert_called_once()
        mock_formatter.handle.assert_called_once_with({"id": 1})
        mock_repo.delete.assert_called_once_with(return_memo)
        mock_output.output.assert_not_called()
        mock_output.error_output.assert_not_called()

    @patch("src.service.memo_service.DeleteMemoFormatterFactory")
    def test_delete_memo_formatter_error(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.side_effect = FormatterError(
            code=FormatterErrorCode.MISSING_REQUIRED_FIELD,
            message="Missing required field",
            original_exception=None,
        )

        mock_formatter_factory_instance = Mock()
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_output = Mock()

        memo_service = MemoService(memo_repo=Mock())
        memo_service.set_output(mock_output)
        memo_service.delete_memo({"id": 1})

        mock_output.output.assert_not_called()
        mock_output.error_output.assert_called_once_with(
            FormatterErrorCode.MISSING_REQUIRED_FIELD.value,
            "Missing required field",
        )

    @patch("src.service.memo_service.DeleteMemoFormatterFactory")
    def test_delete_memo_repository_error(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.return_value = {"id": 1}

        mock_formatter_factory_instance = Mock()
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_repo = Mock(spec=MemoRepositoryInterface)
        mock_repo.get.side_effect = RepositoryError(
            code=RepositoryErrorCode.FAILED_TO_DELETE_MEMO,
            message="Failed to delete memo",
            original_exception=None,
        )

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.delete_memo({"id": 1})
        mock_output.output.assert_not_called()
        mock_output.error_output.assert_called_once_with(
            RepositoryErrorCode.FAILED_TO_DELETE_MEMO.value,
            "Failed to delete memo",
        )

    @patch("src.service.memo_service.DeleteMemoFormatterFactory")
    def test_delete_memo_not_found(self, mock_formatter_factory):
        mock_formatter = Mock()
        mock_formatter.handle.return_value = {"id": 1}

        mock_formatter_factory_instance = Mock()
        mock_formatter_factory_instance.create.return_value = mock_formatter
        mock_formatter_factory.return_value = mock_formatter_factory_instance

        mock_repo = Mock(spec=MemoRepositoryInterface)
        mock_repo.get.return_value = None

        mock_output = Mock()

        memo_service = MemoService(memo_repo=mock_repo)
        memo_service.set_output(mock_output)
        memo_service.delete_memo({"id": 1})

        mock_repo.delete.assert_not_called()
        mock_output.output.assert_not_called()
        mock_output.error_output.assert_not_called()


if __name__ == "__main__":
    unittest.main()
