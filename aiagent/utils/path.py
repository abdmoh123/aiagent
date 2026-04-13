"""Path related functions and data structures."""

import os
from enum import StrEnum


class PathType(StrEnum):
    """Enums for path types."""
    DIRECTORY = "directory"
    FILE = "file"


def combine_paths(working_directory: str, path: str) -> str:
    """Combines a working directory and a path.

    Args:
        working_directory: The working directory.
        path: The path to combine.

    Returns:
        The combined path.
    """
    working_dir_abs = os.path.abspath(working_directory)
    return os.path.normpath(os.path.join(working_dir_abs, path))


def create_dirs_with_parents(path: str) -> None:
    """Creates parent directories if they don't exist.

    Handles both file and directory paths.

    Args:
        path: The path to create parent directories for.
    """
    if os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
        return

    os.makedirs(os.path.dirname(path), exist_ok=True)
