"""Tests for the get_files_info module."""

from aiagent.functions.get_files_info import get_files_info

calculator_path: str = "aiagent/calculator"

current_result: str = get_files_info(calculator_path, ".")
pkg_result: str = get_files_info(calculator_path, "pkg")
bin_result: str = get_files_info(calculator_path, "/bin")
parent_result: str = get_files_info(calculator_path, "../")

results = [current_result, pkg_result, bin_result, parent_result]

for result in results:
    print(result)
