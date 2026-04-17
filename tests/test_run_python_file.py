"""Tests for the run_python_file function."""

from aiagent.functions.run_python_file import run_python_file

calculator_path: str = "aiagent/calculator"

main_result: str = run_python_file(calculator_path, "main.py")
main_35_result: str = run_python_file(calculator_path, "main.py", ["3 + 5"])
test_result: str = run_python_file(calculator_path, "tests.py")
outside_result: str = run_python_file(calculator_path, "../main.py")
nonexistent_result: str = run_python_file(calculator_path, "nonexistent.py")
txt_file_result: str = run_python_file(calculator_path, "lorem.txt")

results = [main_result, main_35_result, test_result, outside_result, nonexistent_result, txt_file_result]

for result in results:
    print(result)
