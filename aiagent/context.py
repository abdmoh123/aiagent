"""Singleton representing the context of a model."""

from collections.abc import Iterable
from typing import Self

from google.genai.types import Content


class Context:
    """Singleton representing the context of a model."""

    __instance: Self | None = None
    __messages: list[Content] = []

    def __new__(cls) -> Self:
        """Return or generate the singleton instance.

        Returns:
            The singleton instance (always the same object).
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @property
    def messages(self) -> tuple[Content, ...]:
        """The message history of the running agent.

        Returns:
            A readonly tuple to prevent tampering with the message history.
        """
        return tuple(self.__messages)

    def add_message(self, message: Content) -> None:
        """Add a message to the context.

        Args:
            message: The message to add.
        """
        self.__messages.append(message)

    def add_messages(self, messages: Iterable[Content]) -> None:
        """Add multiple messages to the context.

        Args:
            messages: The messages to add.
        """
        self.__messages.extend(messages)
