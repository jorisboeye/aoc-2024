from pathlib import Path
from typing import Generator

import pytest

FILE = Path(__file__)
TEST_RESULT = 9
TEST_INPUT = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def mas_generator(puzzle_input: str) -> Generator[bool, None, None]:
    lines = puzzle_input.splitlines()
    for l_idx, line in enumerate(lines[1:-1], start=1):
        for c_idx, char in enumerate(line[1:-1], start=1):
            if char == "A":
                left_diagonal = "".join(
                    [lines[l_idx + 1][c_idx - 1], lines[l_idx - 1][c_idx + 1]]
                )
                right_diagonal = "".join(
                    [lines[l_idx - 1][c_idx - 1], lines[l_idx + 1][c_idx + 1]]
                )
                yield left_diagonal in ("MS", "SM") and right_diagonal in ("MS", "SM")


def solve(puzzle_input: str | Path) -> int:
    return sum(mas_generator(puzzle_input=puzzle_input))


@pytest.mark.parametrize(
    ("test_input", "expected"),
    ((TEST_INPUT, TEST_RESULT),),
)
def test_solve(test_input: str, expected: int) -> None:
    assert solve(test_input) == expected


if __name__ == "__main__":
    test_answer = solve(puzzle_input=TEST_INPUT)
    print(test_answer)
    if test_answer == TEST_RESULT:
        with open(FILE.parent / "input.txt") as file:
            answer = solve(puzzle_input=file.read())
        print(answer)
