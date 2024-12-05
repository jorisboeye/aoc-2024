from collections.abc import Generator
from collections.abc import Sequence
from pathlib import Path

import pytest

FILE = Path(__file__)
TEST_RESULT = 18
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

SECOND_TEST_RESULT = 1
SECOND_TEST_INPUT = """\
XDDD
DMDD
DDAD
DDDS
"""


def counter(lines: Sequence[str]) -> Generator[int, None, None]:
    for line in lines:
        yield line.count("XMAS") + line.count("SAMX")


def get_vertical(puzzle_input: str) -> Sequence[str]:
    return ["".join(line_chars) for line_chars in zip(*puzzle_input.splitlines())]


def get_reversed(lines: Sequence[str]) -> Sequence[str]:
    return ["".join(reversed(line)) for line in lines]


def get_diagonals(lines: Sequence[str]) -> Generator[str, None, None]:
    l_lim = len(lines)
    c_lim = len(lines[0])
    for char in range(c_lim - 3):
        diagonal = []
        for l_idx, c_idx in zip(range(l_lim), range(char, c_lim)):
            diagonal.append(lines[l_idx][c_idx])
        yield "".join(diagonal)
    for line in range(1, l_lim - 3):
        diagonal = []
        for l_idx, c_idx in zip(range(line, l_lim), range(c_lim)):
            diagonal.append(lines[l_idx][c_idx])
        yield "".join(diagonal)


def solve(puzzle_input: str) -> int:
    horizontal = puzzle_input.splitlines()
    vertical = get_vertical(puzzle_input=puzzle_input)
    right_diagonal = list(get_diagonals(horizontal))
    left_diagonal = list(get_diagonals(get_reversed(horizontal)))
    result = (
        sum(counter(horizontal))
        + sum(counter(vertical))
        + sum(counter(right_diagonal))
        + sum(counter(left_diagonal))
    )
    return result


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        (TEST_INPUT, TEST_RESULT),
        (SECOND_TEST_INPUT, SECOND_TEST_RESULT),
    ),
)
def test_solve(test_input: str, expected: int) -> None:
    assert solve(test_input) == expected


@pytest.mark.parametrize(
    ("test_input", "expected"), ((SECOND_TEST_INPUT, ["XDDD", "DMDD", "DDAD", "DDDS"]),)
)
def test_vertical(test_input: str, expected: Sequence[str]) -> None:
    assert get_vertical(test_input) == expected


def test_get_reversed() -> None:
    lines = ["XDDD", "DMDD", "DDAD", "DDDS"]
    expected = ["DDDX", "DDMD", "DADD", "SDDD"]
    assert get_reversed(lines) == expected


if __name__ == "__main__":
    test_answer = solve(puzzle_input=TEST_INPUT)
    print(test_answer)
    if test_answer == TEST_RESULT:
        with open(FILE.parent / "input.txt") as file:
            answer = solve(puzzle_input=file.read())
        print(answer)
