from pathlib import Path

import pytest

FILE = Path(__file__)
TEST_RESULT = 4
TEST_INPUT = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def validate_line(levels: list[int]) -> bool:
    diff = [c - n for c, n in zip(levels, levels[1:])]
    return all(4 > d > 0 for d in diff) or all(-4 < d < 0 for d in diff)


def solve(puzzle_input: str | Path) -> int:
    safe = 0
    for line in puzzle_input.splitlines():
        numbers = list(map(int, line.split()))
        for i, _ in enumerate(numbers):
            dampened = [n for j, n in enumerate(numbers) if j != i]
            if validate_line(dampened):
                safe += 1
                break
    return safe


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
