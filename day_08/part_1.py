from __future__ import annotations

import os
import re
from itertools import cycle


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def solve(data: str) -> int:
    instructions, rest = data.split('\n\n')

    pattern = re.compile(r'(?P<node>\w+) = \((?P<l>\w+), (?P<r>\w+)\)')

    nodes: dict[str, dict[str, str]] = {}
    for line in rest.splitlines():
        m = pattern.fullmatch(line)
        assert m is not None

        nodes[m['node']] = {'L': m['l'], 'R': m['r']}

    node = 'AAA'
    for i, instruction in enumerate(cycle(instructions), 1):
        node = nodes[node][instruction]
        if node == 'ZZZ':
            steps = i
            break

    return steps


TEST_DATA_1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

TEST_DATA_2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

assert solve(TEST_DATA_1) == 2
assert solve(TEST_DATA_2) == 6

print(solve(INPUT_DATA))  # 21409
