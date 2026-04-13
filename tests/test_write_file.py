"""Tests for the write_file function."""

from aiagent.functions.write_file import write_file

lorem_result: str = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
morelorem_result: str = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
temp_result: str = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

results = [lorem_result, morelorem_result, temp_result]

for result in results:
    print(result)
