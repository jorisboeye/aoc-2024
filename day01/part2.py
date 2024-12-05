from pathlib import Path

import pytest

FILE = Path(__file__)
TEST_RESULT = 31
TEST_INPUT = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""


def solve(puzzle_input: str) -> int:
    left, right = [], []
    for line in puzzle_input.splitlines():
        left_value, right_value = map(int, line.split())
        left.append(left_value)
        right.append(right_value)
    return sum(l_v * sum(r_v == l_v for r_v in right) for l_v in left)


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
