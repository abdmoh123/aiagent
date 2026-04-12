"""Function for getting file information."""

import os

from aiagent.utils.path import PathType, combine_paths
from aiagent.utils.validation import (
    generate_error_message,
    is_path_in_working_dir,
    is_path_type_valid,
)


def __generate_error_message(message: str) -> str:
    """Generates an error message in a consistent format with 4 space indent.

    Args:
        message: An error message.

    Returns:
        The formatted error message with 4 space indent.
    """
    return generate_error_message(message, indent=4)


def get_files_info(working_directory: str, directory: str = ".") -> str:
    """Function for getting file information.

    Args:
        working_directory: The working directory.
        directory: The directory to list.

    Returns:
        An output string showing all the files in the directory with size and type.
        Or an error message if something went wrong.
    """
    # If directory is '.', the output strings will refer to it as the current directory
    display_dir: str = f"'{directory}'" if directory != "." else "current"
    output_string = f"Result for {display_dir} directory:\n"

    # Ensure the given directory is inside the working directory
    if not is_path_in_working_dir(working_directory, directory):
        output_string += __generate_error_message(f'Cannot list "{directory}" as it is outside the permitted working directory')
        return output_string

    target_dir = combine_paths(working_directory, directory)
    if not is_path_type_valid(PathType.DIRECTORY, target_dir):
        output_string += __generate_error_message(f"{directory} is not a directory")
        return output_string

    # Prepare the output string data
    try:
        item_names: list[str] = os.listdir(target_dir)
        item_sizes: list[int] = [os.path.getsize(os.path.join(target_dir, item)) for item in item_names]
        item_types: list[bool] = [os.path.isdir(os.path.join(target_dir, item)) for item in item_names]
    except Exception:
        output_string += __generate_error_message(f"{target_dir} does not exist")
        return output_string

    # Add the data to the output string
    for item_name, file_size, is_dir in zip(item_names, item_sizes, item_types):
        output_string += f"  - {item_name}: {file_size=} bytes, {is_dir=}\n"
    return output_string
