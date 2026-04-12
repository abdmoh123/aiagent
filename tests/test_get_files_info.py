"""Tests for the get_files_info module."""

from aiagent.functions.get_files_info import get_files_info

current_result: str = get_files_info("calculator", ".")
pkg_result: str = get_files_info("calculator", "pkg")
bin_result: str = get_files_info("calculator", "/bin")
parent_result: str = get_files_info("calculator", "../")

results = [current_result, pkg_result, bin_result, parent_result]

for result in results:
    print(result)
