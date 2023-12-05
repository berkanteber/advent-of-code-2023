from __future__ import annotations

import os
import re
from collections import defaultdict
from itertools import pairwise


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


class RangeDict:
    def __init__(self) -> None:
        self.ranges: list[tuple[int, int, int]] = []

    def add_range(self, src_start: int, dst_start: int, count: int) -> None:
        self.ranges.append((src_start, dst_start, count))

    def get(self, key: int) -> int:
        for src_start, dst_start, count in self.ranges:
            if src_start <= key < src_start + count:
                return key + (dst_start - src_start)
        return key


def solve(data: str) -> int:
    seeds: set[int]
    maps: defaultdict[tuple[str, str], RangeDict] = defaultdict(RangeDict)

    for section in data.split('\n\n'):
        header, nums = map(str.strip, section.split(':'))
        if header == 'seeds':
            seeds = set(map(int, nums.split()))
        else:
            m = re.match(r'(?P<src>\w+)-to-(?P<dst>\w+) map', header)
            assert m is not None

            key = (m['src'], m['dst'])
            for line in nums.splitlines():
                dst_start, src_start, count = map(int, line.split())
                maps[key].add_range(src_start, dst_start, count)

    map_steps = (
        'seed',
        'soil',
        'fertilizer',
        'water',
        'light',
        'temperature',
        'humidity',
        'location',
    )

    locations: list[int] = []
    for seed in seeds:
        current = seed
        for map_key in pairwise(map_steps):
            current = maps[map_key].get(current)
        else:
            locations.append(current)

    return min(locations)


TEST_DATA = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

assert solve(TEST_DATA) == 35

print(solve(INPUT_DATA))  # 88151870
