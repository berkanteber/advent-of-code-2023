from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def solve(data: str) -> int:
    l1, l2 = data.splitlines()

    time = int(''.join(l1.split()[1:]))
    record = int(''.join(l2.split()[1:]))

    first_win: int
    for sec in range(time):
        if sec * (time - sec) <= record:
            continue

        first_win = sec
        break

    last_win = time - first_win

    assert last_win >= first_win
    wins = last_win - first_win + 1

    return wins


TEST_DATA = """\
Time:      7  15   30
Distance:  9  40  200
"""

assert solve(TEST_DATA) == 71503

print(solve(INPUT_DATA))  # 28360140
