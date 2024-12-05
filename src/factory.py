"""Factory module to create MemoNest instances for different use cases."""

import sqlite3
from enum import Enum, auto

from src.interaction import MemoNest, MemoryOutput, OutputHandler
from src.repository.memo_repository import MemoRepositoryInterface, SQLiteMemoRepository
from src.service.memo_service import MemoService


class MemoNestMode(Enum):
    """Define the different modes for MemoNest creation."""

    SINGLE_USER = auto()  # 單人單機模式
    COLLABORATION = auto()  # 多人協作模式
    ISOLATION = auto()  # 多人隔離模式


class MemoNestFactory:
    """
    A factory to create MemoNest instances with appropriate configurations for different use cases.
    It supports three modes:
    1. Single-user mode (single instance for all components)
    2. Multi-user collaboration mode (single MemoRepository, new MemoNest and OutputHandler)
    3. Multi-user isolation mode (new MemoNest, MemoRepository, and OutputHandler)
    """

    def __init__(self) -> None:
        """
        Initializes the factory with the provided database connection.
        """
        self.database_connection = None
        self.memo_repo = None
        self.memo_nest = None
        self.output_handler = None

    def create_memo_nest(self, mode: MemoNestMode) -> MemoNest:
        """
        Create a MemoNest instance based on the mode.

        Args:
            mode (MemoNestMode): The mode of operation.
            Can be MemoNestMode.SINGLE_USER, MemoNestMode.COLLABORATION, or MemoNestMode.ISOLATION.

        Returns:
            MemoNest: A configured MemoNest instance.
        """

        if mode == MemoNestMode.SINGLE_USER:
            return self.get_singleton_memo_nest()

        if mode == MemoNestMode.COLLABORATION:
            return self.get_shared_memo_nest()

        if mode == MemoNestMode.ISOLATION:
            return self.get_isolation_memo_nest()

        raise ValueError(f"Invalid mode: {mode}")

    def get_singleton_memo_nest(self) -> MemoNest:
        """Return a single instance of MemoRepository for the single-user mode."""

        if self.memo_nest is None:
            self.memo_nest = MemoService(self.get_singleton_memo_repository())
            self.memo_nest.set_output(self.get_singleton_output_handler())

        return self.memo_nest

    def get_shared_memo_nest(self) -> MemoNest:
        """Return a new MemoNest instance each time in collaboration mode."""

        memo_repo = self.get_singleton_memo_repository()
        memo_nest = MemoService(memo_repo)
        output_handler = self.get_new_output_handler()
        memo_nest.set_output(output_handler)

        return memo_nest

    def get_isolation_memo_nest(self) -> MemoNest:
        """Return a new MemoNest instance each time in isolation mode."""

        memo_repo = self.get_new_memo_repository()
        memo_nest = MemoService(memo_repo)
        output_handler = self.get_new_output_handler()
        memo_nest.set_output(output_handler)

        return memo_nest

    def get_singleton_memo_repository(self) -> MemoRepositoryInterface:
        """Return a single instance of MemoRepository for the single-user mode."""

        if self.memo_repo is None:
            self.memo_repo = SQLiteMemoRepository(
                self.get_singleton_database_connection()
            )
            self.memo_repo.create_table_if_not_exists()

        return self.memo_repo

    def get_new_memo_repository(self) -> MemoRepositoryInterface:
        """Return a new MemoRepository instance each time in isolation mode."""

        memo_repo = SQLiteMemoRepository(self.get_new_database_connection())
        memo_repo.create_table_if_not_exists()

        return memo_repo

    def get_singleton_database_connection(self) -> sqlite3.Connection:
        """Return a single instance of the database connection for the single-user mode."""

        if self.database_connection is None:
            self.database_connection = sqlite3.connect(":memory:")

        return self.database_connection

    def get_new_database_connection(self) -> sqlite3.Connection:
        """Return a new database connection each time in isolation mode."""

        return sqlite3.connect(":memory:")

    def get_singleton_output_handler(self) -> OutputHandler:
        """Return a single instance of OutputHandler for the single-user mode."""

        if self.output_handler is None:
            self.output_handler = MemoryOutput()

        return self.output_handler

    def get_new_output_handler(self) -> OutputHandler:
        """Return a new OutputHandler instance each time in isolation mode."""

        return MemoryOutput()
