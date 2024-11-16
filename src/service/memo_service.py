"""A module for managing memo-related use cases."""

from src.entity.memo import Memo
from src.formatter.common import FormatterError
from src.formatter.memo_formatter import (
    AddMemoFormatterFactory,
    DeleteMemoFormatterFactory,
    GetMemoFormatterFactory,
    UpdateMemoFormatterFactory,
)
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
            memo = self.memo_repo.get(memo_id)

            self.output({"memo": memo.to_dict()})

        except (FormatterError, RepositoryError) as error:
            self.error(error.code.value, error.code.get_message())

    def get_memo(self, data: dict) -> None:
        try:
            formatter = GetMemoFormatterFactory().create()
            data = formatter.handle(data)

            memo = self.memo_repo.get(data["id"])

            if memo is None:
                self.output({})
            else:
                self.output({"memo": memo.to_dict()})

        except (FormatterError, RepositoryError) as error:
            self.error(error.code.value, error.code.get_message())

    def get_memos(self) -> None:
        try:
            memos = self.memo_repo.get_all()
            memos = [memo.to_dict() for memo in memos]
            self.output({"list": memos})

        except RepositoryError as error:
            self.error(error.code.value, error.code.get_message())

    def update_memo(self, data: dict) -> None:
        try:
            formatter = UpdateMemoFormatterFactory().create()
            data = formatter.handle(data)

            memo = Memo(id=data["id"], title=data["title"])
            self.memo_repo.update(memo)
            memo = self.memo_repo.get(data["id"])

            if memo is None:
                self.output({})
            else:
                self.output({"memo": memo.to_dict()})

        except (FormatterError, RepositoryError) as error:
            self.error(error.code.value, error.code.get_message())

    def delete_memo(self, data: dict) -> None:
        try:
            formatter = DeleteMemoFormatterFactory().create()
            data = formatter.handle(data)

            memo = self.memo_repo.get(data["id"])
            if memo is not None:
                self.memo_repo.delete(memo)

        except (FormatterError, RepositoryError) as error:
            self.error(error.code.value, error.code.get_message())
