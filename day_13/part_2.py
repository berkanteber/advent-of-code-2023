from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def _check(lst: list[str], i: int) -> bool:
    found = False
    for r1, r2 in zip(lst[i::-1], lst[i+1:]):
        for ch1, ch2 in zip(r1, r2):
            if ch1 != ch2:
                if found:
                    return False
                else:
                    found = True

    return found


def _calculate(lst: list[str]) -> int:
    for i in range(len(lst)):
        if _check(lst, i):
            return i + 1
    else:
        return 0


def solve(data: str) -> int:
    patterns = data.split('\n\n')

    total = 0
    for pattern in patterns:
        rows = pattern.splitlines()
        cols = [''.join(col_lst) for col_lst in zip(*rows)]

        total += 100 * _calculate(rows) + _calculate(cols)

    return total


TEST_DATA = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

assert solve(TEST_DATA) == 400

print(solve(INPUT_DATA))  # 37876
