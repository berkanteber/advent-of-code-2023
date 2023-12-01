from __future__ import annotations

import os
from functools import cache


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


@cache
def _reverse(s: str) -> str:
    return ''.join(reversed(s))


def solve(data: str) -> int:
    digits = tuple(map(str, range(10)))
    names = (
        'one',
        'two',
        'three',
        'four',
        'five',
        'six',
        'seven',
        'eight',
        'nine',
    )
    digits_or_names = {
        **{digit: i for i, digit in enumerate(digits, 0)},
        **{name: i for i, name in enumerate(names, 1)},
    }

    total = 0
    for line in data.splitlines():
        first_places = [
            (idx, dn) for dn in digits_or_names
            if (idx := line.find(dn)) != -1
        ]
        _, first = min(first_places)

        last_places = [
            (idx, dn) for dn in digits_or_names
            if (idx := _reverse(line).find(_reverse(dn))) != -1
        ]
        _, last = min(last_places)

        total += digits_or_names[first] * 10 + digits_or_names[last]

    return total


TEST_DATA = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

assert solve(TEST_DATA) == 281

print(solve(INPUT_DATA))  # 53340
