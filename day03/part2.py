import re
from pathlib import Path

import pytest

FILE = Path(__file__)
TEST_RESULT = 48
TEST_INPUT = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""


def generate_multiplication(input_string) -> int:
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    enabled = True
    while input_string:
        if enabled:
            data, _, input_string = input_string.partition("don't()")
            enabled = False
            yield sum(int(a) * int(b) for a, b in pattern.findall(data))
        else:
            _, _, input_string = input_string.partition("do()")
            enabled = True


def solve(puzzle_input: str | Path) -> int:
    puzzle_input = "".join(puzzle_input.splitlines())
    return sum(generate_multiplication(puzzle_input))


@pytest.mark.parametrize(
    ("test_input", "expected"),
    ((TEST_INPUT, TEST_RESULT),),
)
def test(test_input: str, expected: int) -> None:
    assert solve(test_input) == expected


if __name__ == "__main__":
    test_answer = solve(puzzle_input=TEST_INPUT)
    print(test_answer)
    if test_answer == TEST_RESULT:
        with open(FILE.parent / "input.txt") as file:
            answer = solve(puzzle_input=file.read())
        print(answer)
