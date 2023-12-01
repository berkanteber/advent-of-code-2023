from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def solve(data: str) -> int:
    digits = set(map(str, range(10)))

    total = 0
    for line in data.splitlines():
        only_digits = [int(ch) for ch in line if ch in digits]
        total += only_digits[0] * 10 + only_digits[-1]

    return total


TEST_DATA = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

assert solve(TEST_DATA) == 142

print(solve(INPUT_DATA))  # 52974
