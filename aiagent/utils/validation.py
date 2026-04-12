"""Various utility functions to reduce code duplication."""

import os

from aiagent.utils.path import PathType, combine_paths


def generate_error_message(message: str, indent: int = 0) -> str:
    """Generates an error message in a consistent format.

    Args:
        message: An error message.
        indent: An optional indentation level, defaults to 0.

    Returns:
        The formatted error message.
    """
    indentation: str = " " * indent
    return f"{indentation}Error: {message}\n"


def is_path_in_working_dir(working_directory: str, path: str) -> bool:
    """Validates if a path is inside the working directory and is a file/directory.

    Args:
        working_directory: The working directory.
        path: The path to validate.

    Returns:
        True if the path is inside the working directory and False otherwise.
    """
    # Ensure the given directory is inside the working directory
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = combine_paths(working_directory, path)
    if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
        return False

    return True

def is_path_type_valid(path_type: PathType, path: str) -> bool:
    """Validates if a path is a file or directory.

    Args:
        path_type: Type the path should be (i.e. file or directory).
        path: The path to validate.

    Returns:
        True if the path matches the given path type and False otherwise.
    """
    is_file: bool = path_type == PathType.FILE
    if os.path.isfile(path) != is_file:
        return False

    return True
