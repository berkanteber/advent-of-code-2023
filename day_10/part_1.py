from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def _adj(ch: str, pos: tuple[int, int]) -> list[tuple[int, int]]:
    r, c = pos

    match ch:
        case '|':
            return [(r+1, c), (r-1, c)]
        case '-':
            return [(r, c+1), (r, c-1)]
        case 'L':
            return [(r-1, c), (r, c+1)]
        case 'J':
            return [(r, c-1), (r-1, c)]
        case '7':
            return [(r, c-1), (r+1, c)]
        case 'F':
            return [(r, c+1), (r+1, c)]
        case 'S':
            return [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        case _:
            return []


def _can_connect(
    diagram: list[list[str]],
    pos1: tuple[int, int],
    pos2: tuple[int, int],
) -> bool:
    r1, c1 = pos1
    ch1 = diagram[r1][c1]

    r2, c2 = pos2
    ch2 = diagram[r2][c2]

    return pos1 in _adj(ch2, pos2) and pos2 in _adj(ch1, pos1)


def _nexts(diagram: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    r, c = pos

    len_row = len(diagram)
    len_col = len(diagram[0])

    return [
        (nr, nc) for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        if 0 <= nr < len_row and 0 <= nc < len_col
        and _can_connect(diagram, pos, (nr, nc))
    ]


def solve(data: str) -> int:
    diagram = [[ch for ch in line] for line in data.splitlines()]

    for row, line in enumerate(diagram):
        for col, cell in enumerate(line):
            if cell == 'S':
                start = row, col

    nexts = [[start, n] for n in _nexts(diagram, start)]
    while nexts:
        route = nexts.pop()
        last = route[-1]

        lnexts = _nexts(diagram, last)
        if len(route) != 2 and start in lnexts:
            break

        nexts += [route + [ln] for ln in lnexts if ln not in route]

    return len(route) // 2


TEST_DATA_1 = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""

TEST_DATA_2 = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

assert solve(TEST_DATA_1) == 4
assert solve(TEST_DATA_2) == 8

print(solve(INPUT_DATA))  # 6947
