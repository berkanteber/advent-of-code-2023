from __future__ import annotations

import os
import re
from collections.abc import Iterator


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def _all(original: str) -> Iterator[str]:
    try:
        idx = original.index('?')
    except ValueError:
        yield original
    else:
        yield from _all(original[:idx] + '.' + original[idx+1:])
        yield from _all(original[:idx] + '#' + original[idx+1:])


def solve(data: str) -> int:
    total = 0
    for line in data.splitlines():
        original, nums_s = line.split()

        end = r'\.*'
        mid = r'\.+'.join(
            rf'#{{{num}}}' for num in map(int, nums_s.split(','))
        )
        pattern = re.compile(rf'{end}{mid}{end}')

        for possibility in _all(original):
            if pattern.fullmatch(possibility):
                total += 1

    return total


TEST_DATA = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

assert solve(TEST_DATA) == 21

print(solve(INPUT_DATA))  # 8270
