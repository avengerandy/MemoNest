"""A module for defining use cases and output interfaces to interact with clients."""

from abc import ABC, abstractmethod
from typing import TypedDict


class OutputHandler(ABC):
    """
    An interface for handling output operations.

    This abstract class allows different output mechanisms (e.g., console, UI, network)
    to be injected into the system. This helps decouple the core application logic from
    the specifics of how data is presented or transmitted.
    """

    @abstractmethod
    def output(self, data: dict) -> None:
        """Handles the task of outputting data, such as presenting it to the user or storing it."""

    @abstractmethod
    def error_output(self, code: int, message: str) -> None:
        """Handles the task of error message, such as raise an error or log it."""


class ConsoleOutput(OutputHandler):
    """An output handler that displays data to the console."""

    def output(self, data: dict) -> None:
        """Outputs the data to the console."""
        print(data)

    def error_output(self, code: int, message: str) -> None:
        """Outputs the error message to the console."""
        print(f"Error code {code}: {message}")


class MemoryOutput(OutputHandler):
    """An output handler that stores data in memory."""

    def __init__(self) -> None:
        self.data = {}

    def output(self, data: dict) -> None:
        self.data.update(data)

    def error_output(self, code: int, message: str) -> None:
        self.data.update({"error": f"Error code {code}: {message}"})


class MemoCreateData(TypedDict):
    """A type for the data required to create a memo."""

    title: str


class MemoUpdateData(TypedDict):
    """A type for the data required to update a memo."""

    id: int
    title: str


class MemoGetData(TypedDict):
    """A type for the data required to retrieve a memo."""

    id: int


class MemoDeleteData(TypedDict):
    """A type for the data required to delete a memo."""

    id: int


class MemoNest(ABC):
    """
    A use case class that manages MemoNest-related operations.

    The MemoNest class encapsulates the business logic for memo operations. It is
    designed to be extended with additional functionality (e.g., updating or deleting
    memos) while delegating output responsibilities to the OutputHandler. This ensures
    that MemoNest is decoupled from any specific output implementation and adheres
    to the Dependency Inversion Principle.
    """

    def __init__(self) -> None:
        self.output_handler = None

    def set_output(self, output: OutputHandler) -> None:
        """
        Sets the output handler to be used for outputting data.

        The output handler is responsible for presenting the result or data
        to the client (UI, database, etc.), following the Dependency Inversion Principle.
        """
        self.output_handler = output

    def output(self, data: dict) -> None:
        """Delegates the task of outputting data to the output handler."""

        if self.output_handler is not None:
            self.output_handler.output(data)

    def error(self, code: int, message: str) -> None:
        """Delegates the task of outputting error data to the output handler."""

        if self.output_handler is not None:
            self.output_handler.error_output(code, message)

    @abstractmethod
    def create_memo(self, data: MemoCreateData) -> None:
        """
        Creates a new memo with the given data.
        """

    @abstractmethod
    def get_memo(self, data: MemoGetData) -> None:
        """Retrieves a memo with the given data."""

    @abstractmethod
    def get_memos(self) -> None:
        """Retrieves all memos."""

    @abstractmethod
    def update_memo(self, data: MemoUpdateData) -> None:
        """Updates an existing memo with the given data."""

    @abstractmethod
    def delete_memo(self, data: MemoDeleteData) -> None:
        """Deletes a memo with the given data."""
