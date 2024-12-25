import unittest
from io import StringIO
from unittest.mock import Mock, patch

from src.interaction import ConsoleOutput, MemoNest, MemoryOutput, OutputHandler


class TestMemoNest(unittest.TestCase):
    def setUp(self):
        class PassImplMemoNest(MemoNest):
            def create_memo(self, data: dict) -> None:
                pass

            def get_memo(self, data: dict) -> None:
                pass

            def get_memos(self) -> None:
                pass

            def update_memo(self, data: dict) -> None:
                pass

            def delete_memo(self, data: dict) -> None:
                pass

        self.memo_nest = PassImplMemoNest()
        self.mock_output_handler = Mock(spec=OutputHandler)
        self.memo_nest.set_output(self.mock_output_handler)

    def test_set_output(self):
        self.memo_nest.set_output(self.mock_output_handler)
        self.assertEqual(self.memo_nest.output_handler, self.mock_output_handler)

    def test_output(self):
        test_data = {"title": "Test Memo", "description": "This is a test memo."}
        self.memo_nest.output(test_data)
        self.mock_output_handler.output.assert_called_once_with(test_data)

        self.memo_nest.set_output(None)
        self.memo_nest.output(test_data)  # not raising an error

    def test_error(self):
        error_code = 404
        error_message = "Not Found"
        self.memo_nest.error(error_code, error_message)
        self.mock_output_handler.error_output.assert_called_once_with(
            error_code, error_message
        )

        self.memo_nest.set_output(None)
        self.memo_nest.error(error_code, error_message)  # not raising an error


class TestConsoleOutput(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    def test_output(self, mock_stdout):
        console_output = ConsoleOutput()
        test_data = {"title": "Test Memo", "description": "This is a test memo."}

        console_output.output(test_data)

        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, str(test_data))

    @patch("sys.stdout", new_callable=StringIO)
    def test_error_output(self, mock_stdout):
        console_output = ConsoleOutput()
        error_code = 404
        error_message = "Not Found"

        console_output.error_output(error_code, error_message)

        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, f"Error code {error_code}: {error_message}")


class TestMemoryOutput(unittest.TestCase):
    def test_output(self):
        memory_output = MemoryOutput()
        test_data = {"title": "Test Memo"}

        memory_output.output(test_data)

        self.assertEqual(memory_output.data, test_data)

    def test_error_output(self):
        memory_output = MemoryOutput()
        error_code = 404
        error_message = "Not Found"

        memory_output.error_output(error_code, error_message)

        self.assertEqual(
            memory_output.data, {"error": f"Error code {error_code}: {error_message}"}
        )


if __name__ == "__main__":
    unittest.main()
