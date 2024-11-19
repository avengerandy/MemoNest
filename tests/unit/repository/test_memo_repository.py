import datetime
import unittest
from unittest.mock import MagicMock, Mock

from src.entity.memo import Memo
from src.repository.common import RepositoryError
from src.repository.memo_repository import SQLiteMemoRepository


class TestSQLiteMemoRepository(unittest.TestCase):

    def setUp(self):
        # MagicMock support the context manager protocol
        self.mock_connection = MagicMock()
        self.repository = SQLiteMemoRepository(self.mock_connection)
        self.now = datetime.datetime.now()
        self.tolerance = datetime.timedelta(seconds=1)

    def assert_time_almost_equal(self, expected_time, actual_time):
        self.assertTrue(
            abs(expected_time - actual_time) <= self.tolerance,
            f"Expected time: {expected_time}, but got: {actual_time}",
        )

    def test_create_memo(self):
        memo = Memo(title="New Memo")

        cursor_mock = Mock()
        cursor_mock.lastrowid = 1
        self.mock_connection.cursor.return_value = cursor_mock

        new_id = self.repository.create(memo)

        self.mock_connection.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once()

        sql, params = cursor_mock.execute.call_args[0]
        expected_sql = (
            "INSERT INTO memos (title, create_date, update_date) VALUES (?, ?, ?)"
        )
        expected_params = (
            memo.title,
            self.now.isoformat(),
            self.now.isoformat(),
        )
        self.assertEqual(sql, expected_sql)
        self.assertEqual(params[0], expected_params[0])

        create_date = datetime.datetime.fromisoformat(params[1])
        update_date = datetime.datetime.fromisoformat(params[2])
        self.assert_time_almost_equal(self.now, create_date)
        self.assert_time_almost_equal(self.now, update_date)
        self.assertEqual(new_id, 1)

    def test_create_memo_error(self):
        memo = Memo(title="New Memo")

        original_exception = Exception("Database error")
        self.mock_connection.cursor.side_effect = original_exception

        with self.assertRaises(RepositoryError) as context:
            self.repository.create(memo)

        self.assertEqual(str(context.exception), "Failed to create memo")
        self.assertEqual(context.exception.original_exception, original_exception)

    def test_update_memo(self):
        memo = Memo(title="Updated Memo", id=1)

        cursor_mock = Mock()
        self.mock_connection.cursor.return_value = cursor_mock

        self.repository.update(memo)

        self.mock_connection.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once()

        sql, params = cursor_mock.execute.call_args[0]
        expected_sql = "UPDATE memos SET title = ?, update_date = ? WHERE id = ?"
        expected_params = (
            memo.title,
            self.now.isoformat(),
            memo.id,
        )
        self.assertEqual(sql, expected_sql)
        self.assertEqual(params[0], expected_params[0])
        self.assertEqual(params[2], expected_params[2])

        update_date = datetime.datetime.fromisoformat(params[1])
        self.assert_time_almost_equal(self.now, update_date)

    def test_update_memo_error(self):
        memo = Memo(title="Updated Memo", id=1)

        original_exception = Exception("Database error")
        self.mock_connection.cursor.side_effect = original_exception

        with self.assertRaises(RepositoryError) as context:
            self.repository.update(memo)

        self.assertEqual(str(context.exception), "Failed to update memo")
        self.assertEqual(context.exception.original_exception, original_exception)

    def test_delete_memo(self):
        memo = Memo(
            id=1,
            title="Memo to delete",
            create_date=datetime.datetime.now(),
            update_date=datetime.datetime.now(),
        )

        cursor_mock = Mock()
        self.mock_connection.cursor.return_value = cursor_mock

        self.repository.delete(memo)

        self.mock_connection.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once()

        sql, params = cursor_mock.execute.call_args[0]
        expected_sql = "DELETE FROM memos WHERE id = ?"
        expected_params = (memo.id,)
        self.assertEqual(sql, expected_sql)
        self.assertEqual(params, expected_params)

    def test_delete_memo_error(self):
        memo = Memo(
            id=1,
            title="Memo to delete",
            create_date=datetime.datetime.now(),
            update_date=datetime.datetime.now(),
        )

        original_exception = Exception("Database error")
        self.mock_connection.cursor.side_effect = original_exception

        with self.assertRaises(RepositoryError) as context:
            self.repository.delete(memo)

        self.assertEqual(str(context.exception), "Failed to delete memo")
        self.assertEqual(context.exception.original_exception, original_exception)

    def test_get_memo(self):
        cursor_mock = Mock()
        self.mock_connection.cursor.return_value = cursor_mock
        cursor_mock.fetchone.return_value = (
            1,
            "Sample Memo",
            datetime.datetime.now().isoformat(),
            datetime.datetime.now().isoformat(),
        )

        memo = self.repository.get(1)

        self.mock_connection.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once()

        sql, params = cursor_mock.execute.call_args[0]
        expected_sql = "SELECT * FROM memos WHERE id = ?"
        expected_params = (1,)
        self.assertEqual(sql, expected_sql)
        self.assertEqual(params, expected_params)

        self.assertIsNotNone(memo)
        self.assertEqual(memo.title, "Sample Memo")

    def test_get_memo_not_found(self):
        cursor_mock = Mock()
        self.mock_connection.cursor.return_value = cursor_mock
        cursor_mock.fetchone.return_value = None

        memo = self.repository.get(1)

        self.mock_connection.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once()

        sql, params = cursor_mock.execute.call_args[0]
        expected_sql = "SELECT * FROM memos WHERE id = ?"
        expected_params = (1,)
        self.assertEqual(sql, expected_sql)
        self.assertEqual(params, expected_params)

        self.assertIsNone(memo)

    def test_get_memo_error(self):
        original_exception = Exception("Database error")
        self.mock_connection.cursor.side_effect = original_exception

        with self.assertRaises(RepositoryError) as context:
            self.repository.get(1)

        self.assertEqual(str(context.exception), "Failed to get memo")
        self.assertEqual(context.exception.original_exception, original_exception)

    def test_get_all_memos(self):
        cursor_mock = Mock()
        self.mock_connection.cursor.return_value = cursor_mock
        cursor_mock.fetchall.return_value = [
            (
                1,
                "Memo 1",
                datetime.datetime.now().isoformat(),
                datetime.datetime.now().isoformat(),
            ),
            (
                2,
                "Memo 2",
                datetime.datetime.now().isoformat(),
                datetime.datetime.now().isoformat(),
            ),
        ]

        memos = self.repository.get_all()

        self.mock_connection.cursor.assert_called_once()
        cursor_mock.execute.assert_called_once()

        sql = cursor_mock.execute.call_args[0][0]
        expected_sql = "SELECT * FROM memos"
        self.assertEqual(sql, expected_sql)

        self.assertEqual(len(memos), 2)

    def test_get_all_memos_error(self):
        original_exception = Exception("Database error")
        self.mock_connection.cursor.side_effect = original_exception

        with self.assertRaises(RepositoryError) as context:
            self.repository.get_all()

        self.assertEqual(str(context.exception), "Failed to get all memos")
        self.assertEqual(context.exception.original_exception, original_exception)


if __name__ == "__main__":
    unittest.main()
