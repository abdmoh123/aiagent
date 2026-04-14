"""Module containing sets of tools."""

from typing import Callable

from aiagent.functions.get_file_content import (
    get_file_content,
    schema_get_file_content,
)
from aiagent.functions.get_files_info import (
    get_files_info,
    schema_get_files_info,
)
from aiagent.functions.run_python_file import (
    run_python_file,
    schema_run_python_file,
)
from aiagent.functions.write_file import schema_write_file, write_file
from google.genai.types import Content, FunctionCall, Part, Tool

available_functions: Tool = Tool(
    function_declarations=[
        schema_write_file,
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
    ]
)

function_map: dict[str, Callable[..., str]] = {
    "write_file": write_file,
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
}

def call_function(function_call: FunctionCall, verbose: bool = False) -> Content:
    """Calls a function."""
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    func_name: str = function_call.name or ""
    if func_name not in function_map:
        return Content(
            role="tool",
            parts=[
                Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"}
                )
            ],
        )

    # Add working directory argument to args
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"  # always overwrite the working directory

    # Run the function and save the result
    result = function_map[func_name](**args)

    return Content(
        role="tool",
        parts=[
            Part.from_function_response(
                name=func_name,
                response={"result": result},
            )
        ],
    )
