from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def solve(data: str) -> int:
    l1, l2 = data.splitlines()

    times = map(int, l1.split()[1:])
    records = map(int, l2.split()[1:])

    races = list(zip(times, records))

    moe = 1
    for time, record in races:
        wins = 0
        for sec in range(time):
            if sec * (time - sec) > record:
                wins += 1

        moe *= wins

    return moe


TEST_DATA = """\
Time:      7  15   30
Distance:  9  40  200
"""

assert solve(TEST_DATA) == 288

print(solve(INPUT_DATA))  # 449550
