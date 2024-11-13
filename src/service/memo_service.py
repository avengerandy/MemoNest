"""A module for managing memo-related use cases."""

from src.entity.memo import Memo
from src.formatter.common import FormatterError
from src.formatter.memo_formatter import AddMemoFormatterFactory
from src.interaction import MemoNest
from src.repository.common import RepositoryError
from src.repository.memo_repository import MemoRepositoryInterface


class MemoService(MemoNest):
    """
    A service class that implements the MemoNest interface for MemoNest use cases,
    coordinating between the formatter, repository, and output handler.
    """

    def __init__(self, memo_repo: MemoRepositoryInterface) -> None:
        super().__init__()
        self.memo_repo = memo_repo

    def create_memo(self, data: dict) -> None:
        try:
            formatter = AddMemoFormatterFactory().create()
            data = formatter.handle(data)
            memo = Memo(title=data["title"])
            memo_id = self.memo_repo.create(memo)
            self.output({"memo_id": memo_id})

        except (FormatterError, RepositoryError) as error:
            self.error(error.code.value, error.code.get_message())
