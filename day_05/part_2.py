from __future__ import annotations

import os
import re
from collections import defaultdict
from itertools import batched
from itertools import pairwise


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


MAX = 10 ** 20


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


def fill_and_sort(orig: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    tmp = sorted(orig)

    # if necessary, fill [0, min)
    min_s = min(orig)[0]
    if min_s != 0:
        tmp.insert(0, (0, 0, min_s))

    new = []
    for (r1_src, r1_dst, r1_cnt), (r2_src, _, _) in pairwise(tmp):
        # add self
        new.append((r1_src, r1_dst, r1_cnt))

        # fill space
        if r2_src > r1_src + r1_cnt:
            start = r1_src + r1_cnt
            end = r2_src

            new.append((start, start, end - start))
    else:
        # add last
        new.append(tmp[-1])

    # fill [max, inf)
    last_s, _, last_c = new[-1]
    new.append((last_s + last_c, last_s + last_c, MAX))

    return new


def merge(
    this: list[tuple[int, int, int]],
    other: list[tuple[int, int, int]],
) -> list[tuple[int, int, int]]:
    this = fill_and_sort(this)
    other = fill_and_sort(other)

    ranges = []
    for (r1_src, r1_dst, r1_cnt) in this:
        for (r2_src, r2_dst, r2_cnt) in other:
            # self:  [r1_dst, r1_dst + r1_cnt)
            # other: [r2_src, r2_src + r2_cnt)
            r2_start = max(r1_dst, r2_src)
            r2_end = min(r1_dst + r1_cnt, r2_src + r2_cnt)
            if r2_start >= r2_end:
                continue

            r1_diff = r1_dst - r1_src
            r2_diff = r2_dst - r2_src

            r1_start = r2_start - r1_diff
            r1_end = r2_end - r1_diff

            ranges.append((r1_start, r2_start + r2_diff, r1_end - r1_start))

    return fill_and_sort(ranges)


def solve(data: str) -> int:
    seeds = []
    maps: defaultdict[tuple[str, str], RangeDict] = defaultdict(RangeDict)

    for section in data.split('\n\n'):
        header, nums = map(str.strip, section.split(':'))
        if header == 'seeds':
            for start, count in batched(map(int, nums.split()), 2):
                seeds.append((start, count))
        else:
            m = re.match(r'(?P<src>\w+)-to-(?P<dst>\w+) map', header)
            assert m is not None

            key = (m['src'], m['dst'])
            for line in nums.splitlines():
                dst_start, src_start, count = map(int, line.split())
                maps[key].add_range(src_start, dst_start, count)

    map_steps = [
        'seed',
        'soil',
        'fertilizer',
        'water',
        'light',
        'temperature',
        'humidity',
        'location',
    ]
    while len(map_steps) >= 3:
        ms1, ms2, ms3 = map_steps[-3:]

        rd12 = maps.pop((ms1, ms2))
        rd23 = maps.pop((ms2, ms3))

        rd13 = RangeDict()
        rd13.ranges = merge(rd12.ranges, rd23.ranges)

        maps[(ms1, ms3)] = rd13
        map_steps = map_steps[:-3] + [ms1, ms3]

    _, final_map = maps.popitem()

    locations = []
    for seed, start in seeds:
        current_seed = seed
        while current_seed < seed + start:
            for (r_start, _, count) in final_map.ranges:
                if current_seed >= r_start + count:
                    continue

                if current_seed < r_start:
                    current_seed = r_start
                else:
                    locations.append(final_map.get(current_seed))
                    current_seed = r_start + count
                break
            else:
                break

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


assert solve(TEST_DATA) == 46

print(solve(INPUT_DATA))  # 2008785
