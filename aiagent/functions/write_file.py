"""Functions for writing files."""

import os

from aiagent.utils.path import combine_paths, create_dirs_with_parents
from aiagent.utils.validation import (
    generate_error_message,
    is_path_in_working_dir,
)
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """Function for writing a file.

    Args:
        working_directory: The working directory.
        file_path: The path to the file.
        content: The content to write to the file.

    Returns:
        A success message if the file was written successfully.
        Or an error message if something went wrong.
    """
    if not is_path_in_working_dir(working_directory, file_path):
        return generate_error_message(f'Cannot write to "{file_path}" as it is outside the permitted working directory')

    # Check if file path is an existing directory
    abs_file_path: str = combine_paths(working_directory, file_path)
    if os.path.isdir(abs_file_path):
        return generate_error_message(f'Cannot write to "{file_path}" as it is a directory')

    # Create all parent directories if they don't exist
    try:
        create_dirs_with_parents(abs_file_path)
    except Exception:
        return generate_error_message(f'Failed to create parent directories for "{file_path}"')

    try:
        with open(abs_file_path, "w") as file:
            _ = file.write(content)
    except Exception:
        return generate_error_message(f"Failed to open file: {file_path}")

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
