from __future__ import annotations

import os
import re


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def _exceeded(sets: str) -> bool:
    colors = {'red': 12, 'green': 13, 'blue': 14}
    for s in sets.split(';'):
        for nc in s.split(','):
            num, color = nc.strip().split()
            if int(num) > colors[color]:
                return True

    return False


def solve(data: str) -> int:
    pattern = re.compile(r'Game (?P<game>\d+): (?P<sets>.+)')

    total = 0
    for line in data.splitlines():
        m = pattern.fullmatch(line)
        assert m is not None

        if not _exceeded(m['sets']):
            total += int(m['game'])

    return total


TEST_DATA = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

assert solve(TEST_DATA) == 8

print(solve(INPUT_DATA))  # 2377
