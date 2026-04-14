"""Function for running arbitrary python code."""

import os
import subprocess

from aiagent.utils.path import PathType, combine_paths
from aiagent.utils.validation import (
    generate_error_message,
    is_path_in_working_dir,
    is_path_type_valid,
)
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs an arbitrary python script",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python script to run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the python script",
            ),
        },
    ),
)


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    """Function for running arbitrary python code.

    Args:
        working_directory: The working directory.
        file_path: Path to the python script to run.
        args: Optional list of arguments to pass to the python script.

    Returns:
        The output of the python script.
        Or an error message if something went wrong.
    """
    try:
        if not is_path_in_working_dir(working_directory, file_path):
            return generate_error_message(f'Cannot execute "{file_path}" as it is outside the permitted working directory')

        abs_file_path: str = combine_paths(working_directory, file_path)
        if not is_path_type_valid(PathType.FILE, abs_file_path):
            return generate_error_message(f'Error: "{file_path}" does not exist or is not a regular file')

        if not abs_file_path.endswith(".py"):
            return generate_error_message(f'Error: "{file_path}" is not a Python file')

        command: list[str] = ["python", abs_file_path]
        # Append the optional arguments if they are provided
        if args:
            command.extend(args)

        # Run the python script in the working directory with a timeout of 30s
        res: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            cwd=os.path.abspath(working_directory),
            capture_output=True,
            text=True,
            timeout=30
        )

        if res.returncode != 0:
            return f"Process exited with code {res.returncode}"

        is_stdout_empty = res.stdout.strip() == ""
        is_stderr_empty = res.stderr.strip() == ""
        if is_stdout_empty and is_stderr_empty:
            return "No output produced"

        # Build the output message of the run python script
        output_str: str = ""
        if not is_stdout_empty:
            output_str += f"STDOUT:\n{res.stdout}"
        if not is_stderr_empty:
            output_str += f"\nSTDERR:\n{res.stderr}"
        return output_str
    except Exception as e:
        return generate_error_message(f"executing Python file: {e}")
