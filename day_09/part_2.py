from __future__ import annotations

import os
from itertools import pairwise


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def solve(data: str) -> int:
    total = 0
    for line in data.splitlines():
        nums = list(map(int, line.split()))

        subnums = [nums]
        while not all(n == 0 for n in subnums[-1]):
            subnums.append([])
            for n1, n2 in pairwise(subnums[-2]):
                subnums[-1].append(n2 - n1)

        current = 0
        for n in reversed([sn[0] for sn in subnums if sn]):
            current = n - current

        total += current

    return total


TEST_DATA = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

assert solve(TEST_DATA) == 2

print(solve(INPUT_DATA))  # 913
