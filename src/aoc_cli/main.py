import argparse
import shutil
import sys
from collections.abc import Sequence
from pathlib import Path
from urllib import request

ROOT_FOLDER = Path().cwd()


def get_input(day: int, year: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    with open(ROOT_FOLDER / ".token") as f:
        token = f.read().strip()
    resp = request.urlopen(
        request.Request(url, headers={"Cookie": f"session={token}"}),
    )
    return str(resp.read().decode("utf-8"))


def make_folder(day: int) -> None:
    path = ROOT_FOLDER / f"day{day:02}"
    shutil.copytree(ROOT_FOLDER / "day00", path)


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="advent-of-code")
    parser.add_argument("day", type=int, help="The day to create")
    args = parser.parse_args(argv)
    with open(ROOT_FOLDER / ".year") as f:
        year = int(f.read().strip())
    make_folder(args.day)
    puzzle_input = get_input(day=args.day, year=year)
    with open(ROOT_FOLDER / f"day{args.day:02}/input.txt", "w") as f:
        f.write(puzzle_input)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
