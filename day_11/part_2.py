from __future__ import annotations

import os
from itertools import combinations


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def solve(data: str, expansion: int = 1_000_000) -> int:
    diagram = {
        (row, col): cell
        for row, line in enumerate(data.splitlines())
        for col, cell in enumerate(line)
    }

    len_rows = max(r for r, _ in diagram.keys())
    len_cols = max(c for _, c in diagram.keys())

    galaxies = []
    nonempty_rows = set()
    nonempty_cols = set()
    for (r, c), cell in diagram.items():
        if cell == '#':
            galaxies.append((r, c))
            nonempty_rows.add(r)
            nonempty_cols.add(c)

    empty_rows = set(range(len_rows)) - nonempty_rows
    empty_cols = set(range(len_cols)) - nonempty_cols

    total = 0
    for (g1r, g1c), (g2r, g2c) in combinations(galaxies, 2):
        min_r, max_r = sorted((g1r, g2r))
        min_c, max_c = sorted((g1c, g2c))

        dist = (max_r - min_r) + (max_c - min_c)
        dist += sum((expansion - 1) for r in empty_rows if min_r < r < max_r)
        dist += sum((expansion - 1) for c in empty_cols if min_c < c < max_c)

        total += dist

    return total


TEST_DATA = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

assert solve(TEST_DATA, 10) == 1030
assert solve(TEST_DATA, 100) == 8410

print(solve(INPUT_DATA))  # 710674907809
