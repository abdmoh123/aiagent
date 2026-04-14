"""Module containing sets of tools."""

from aiagent.functions.get_file_content import schema_get_file_content
from aiagent.functions.get_files_info import schema_get_files_info
from aiagent.functions.run_python_file import schema_run_python_file
from aiagent.functions.write_file import schema_write_file
from google.genai.types import Tool

available_functions: Tool = Tool(
    function_declarations=[
        schema_write_file,
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
    ]
)
