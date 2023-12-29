from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def solve(data: str) -> int:
    steps = data.strip().split(',')

    total = 0
    for step in steps:
        current = 0
        for ch in step:
            current += ord(ch)
            current = current * 17 % 256

        total += current

    return total


TEST_DATA = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

assert solve(TEST_DATA) == 1320

print(solve(INPUT_DATA))  # 517015
