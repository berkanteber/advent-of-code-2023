from __future__ import annotations

import os
from itertools import pairwise


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def _calculate(lst: list[str]) -> int:
    for i, (s1, s2) in enumerate(pairwise(lst)):
        if s1 == s2:
            for r1, r2 in zip(lst[i::-1], lst[i+1:]):
                if r1 != r2:
                    break
            else:
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

assert solve(TEST_DATA) == 405

print(solve(INPUT_DATA))  # 30802
