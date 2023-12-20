from __future__ import annotations

import os
from functools import cache


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


@cache
def _until(string: str, idx: int) -> str:
    return string[:idx]


@cache
def _sep(string: str, idx: int) -> str:
    return string[idx:idx+1]


@cache
def _from(string: str, idx: int) -> str:
    return string[idx+1:]


@cache
def _next(string: str) -> str:
    return string[1:]


@cache
def _possible(full_string: str, first_idx: int) -> int:
    string = _until(full_string, first_idx)
    return len(string) == first_idx and '.' not in string


@cache
def _count(string: str, nums: tuple[int, ...]) -> int:
    string = string.strip('.').replace('..', '.')

    if not string:
        return 0

    if not nums:
        if '#' in string:
            return 0
        else:
            return 1

    first, *rest = nums

    match _sep(string, first):
        case '':
            if _possible(string, first) and not rest:
                return 1
            else:
                return 0
        case '.':
            if string[0:1] == '#':
                if _possible(string, first):
                    return _count_from(string, first, rest)
                else:
                    return 0
            elif _possible(string, first):
                return _count_next(string, nums) + _count_from(string, first, rest)
            else:
                return _count_next(string, nums)
        case '#':
            if string[0:1] == '?':
                return _count_next(string, nums)
            else:
                return 0
        case '?':
            s1, s2 = _until(string, first), _from(string, first)
            return _count(f'{s1}.{s2}', nums) + _count(f'{s1}#{s2}', nums)
        case _:
            raise AssertionError


def _count_next(string: str, nums: tuple[int, ...]) -> int:
    return _count(_next(string), nums)


def _count_from(string: str, first: int, rest: list[int]) -> int:
    return _count(_from(string, first), tuple(rest))


def solve(data: str) -> int:
    total = 0
    for line in data.splitlines():
        original, nums_s = line.split()
        original = '?'.join([original] * 5)
        nums = tuple(map(int, nums_s.split(',') * 5))

        total += _count(original, nums)

    return total


TEST_DATA = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

assert solve(TEST_DATA) == 525152

print(solve(INPUT_DATA))  # 204640299929836
