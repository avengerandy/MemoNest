import unittest

from src.repository.common import RepositoryError, RepositoryErrorCode


class TestRepositoryErrorCode(unittest.TestCase):

    def test_enum_values(self):
        self.assertEqual(RepositoryErrorCode.FAILED_TO_CREATE_MEMO.value, 101)
        self.assertEqual(RepositoryErrorCode.FAILED_TO_UPDATE_MEMO.value, 102)
        self.assertEqual(RepositoryErrorCode.FAILED_TO_DELETE_MEMO.value, 103)
        self.assertEqual(RepositoryErrorCode.FAILED_TO_GET_MEMO.value, 104)
        self.assertEqual(RepositoryErrorCode.FAILED_TO_GET_ALL_MEMOS.value, 105)

    def test_get_message(self):
        for code in RepositoryErrorCode:
            expected_message = code.name.lower().replace("_", " ").capitalize()
            self.assertEqual(code.get_message(), expected_message)

    def test_invalid_enum_value(self):
        invalid_status = 999
        with self.assertRaises(ValueError):
            RepositoryErrorCode(invalid_status)


class TestRepositoryError(unittest.TestCase):
    def test_initialization(self):
        original_exception = Exception("Original exception")
        error_code = RepositoryErrorCode.FAILED_TO_CREATE_MEMO
        error_message = error_code.get_message()

        repo_error = RepositoryError(error_code, error_message, original_exception)

        self.assertEqual(repo_error.code, error_code)
        self.assertEqual(str(repo_error), error_message)
        self.assertEqual(repo_error.original_exception, original_exception)


if __name__ == "__main__":
    unittest.main()
