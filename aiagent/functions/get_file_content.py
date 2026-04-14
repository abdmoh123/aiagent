"""Function for getting a file's contents."""

from aiagent.constants import MAX_CHARS
from aiagent.utils.path import PathType, combine_paths
from aiagent.utils.validation import (
    generate_error_message,
    is_path_in_working_dir,
    is_path_type_valid,
)
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read",
            ),
        },
    ),
)


def get_file_content(working_directory: str, file_path: str) -> str:
    """Function for getting a file's contents.

    Args:
        working_directory: The working directory.
        file_path: Path to the file to read.

    Returns:
        The contents of the given file.
        Or an error message if something went wrong.
    """
    if not is_path_in_working_dir(working_directory, file_path):
        return generate_error_message(f'Cannot read "{file_path}" as it is outside the permitted working directory')

    abs_file_path: str = combine_paths(working_directory, file_path)
    if not is_path_type_valid(PathType.FILE, abs_file_path):
        return generate_error_message(f'File not found or is not a regular file: "{file_path}"')

    try:
        with open(abs_file_path, "r") as file:
            contents: str = file.read(MAX_CHARS)
            # If an empty string is returned, after the file was read, then it
            # means that the we reached the end of the file
            if file.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return contents
    except Exception:
        return generate_error_message(f"Failed to open file: {file_path}")

