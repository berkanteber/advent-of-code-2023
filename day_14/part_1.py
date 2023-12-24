from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def _sort(string: str) -> str:
    return ''.join(sorted(string, key=lambda ch: {'O': 0, '.': 1}[ch]))


def _tilt(col: str) -> str:
    parts = []
    for part in col.split('#'):
        parts.append(_sort(part))
    return '#'.join(parts)


def solve(data: str) -> int:
    cols = [''.join(col_lst) for col_lst in zip(*data.splitlines())]
    tilted = [_tilt(col) for col in cols]

    total = 0
    length = len(tilted[0])
    for col in tilted:
        for i, ch in enumerate(col):
            if ch == 'O':
                total += length - i

    return total


TEST_DATA = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

assert solve(TEST_DATA) == 136

print(solve(INPUT_DATA))  # 108144
