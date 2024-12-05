from pathlib import Path

import pytest

FILE = Path(__file__)
TEST_RESULT = 11
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
    return sum(abs(l_v - r_v) for l_v, r_v in zip(sorted(left), sorted(right)))


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
