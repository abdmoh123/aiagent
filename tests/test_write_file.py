"""Tests for the write_file function."""

from aiagent.functions.write_file import write_file

calculator_path: str = "aiagent/calculator"

lorem_result: str = write_file(calculator_path, "lorem.txt", "wait, this isn't lorem ipsum")
morelorem_result: str = write_file(calculator_path, "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
temp_result: str = write_file(calculator_path, "/tmp/temp.txt", "this should not be allowed")

results = [lorem_result, morelorem_result, temp_result]

for result in results:
    print(result)
