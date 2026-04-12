"""Tests for the get_file_content function."""

from aiagent.functions.get_file_content import get_file_content

lorem_result: str = get_file_content("calculator", "lorem.txt")
main_result: str = get_file_content("calculator", "main.py")
calculator_result: str = get_file_content("calculator", "pkg/calculator.py")
cat_result: str = get_file_content("calculator", "/bin/cat")
not_exist_result: str = get_file_content("calculator", "pkg/does_not_exist.py")

results = [lorem_result, main_result, calculator_result, cat_result, not_exist_result]

for result in results:
    print(result)
