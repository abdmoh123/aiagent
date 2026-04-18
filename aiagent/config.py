"""Config module for the ai-agent project."""

import os
from dataclasses import dataclass


@dataclass()
class AppArgs:
    """Dataclass representing the arguments a user can pass through the CLI."""
    user_prompt: str
    verbose: bool = False


def get_env(env_var: str) -> str:
    """Get the value of an environment variable and ensure the result is not None.

    Args:
        env_var: The name of the environment variable to get.

    Returns:
        The value of the environment variable.

    Raises:
        RuntimeError: If the environment variable is not set.
    """
    value: str | None = os.environ.get(env_var)
    if value is None:
        raise RuntimeError(f"Missing {env_var}")
    return value


gemini_api_key = get_env("GEMINI_API_KEY")
