"""Tests for the run_python_file function."""

from aiagent.functions.run_python_file import run_python_file

main_result: str = run_python_file("calculator", "main.py")
main_35_result: str = run_python_file("calculator", "main.py", ["3 + 5"])
test_result: str = run_python_file("calculator", "tests.py")
outside_result: str = run_python_file("calculator", "../main.py")
nonexistent_result: str = run_python_file("calculator", "nonexistent.py")
txt_file_result: str = run_python_file("calculator", "lorem.txt")

results = [main_result, main_35_result, test_result, outside_result, nonexistent_result, txt_file_result]

for result in results:
    print(result)
