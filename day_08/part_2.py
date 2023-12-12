from __future__ import annotations

import os
import re
import time
from collections import defaultdict


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def solve(data: str, *, debug: bool = False) -> int:
    instructions, rest = data.split('\n\n')

    # Longer instructions means more upfront compute, but faster steps later.
    # Find an optimum looking at `avg`. For given input 150 is ~15-20x faster than 1.
    # Performance improvement eventually stops, though upfront cost keeps increasing.
    instructions_multiplier = 150
    instructions *= instructions_multiplier

    pattern = re.compile(r'(?P<node>\w+) = \((?P<l>\w+), (?P<r>\w+)\)')

    nodes: dict[str, dict[str, str]] = {}
    for line in rest.splitlines():
        m = pattern.fullmatch(line)
        assert m is not None

        nodes[m['node']] = {'L': m['l'], 'R': m['r']}

    next_cycle: dict[str, str] = {}
    zs: defaultdict[int, set[str]] = defaultdict(set)
    for node in nodes:
        current = node
        for i, instruction in enumerate(instructions, 1):
            current = nodes[current][instruction]
            if current[-1] == 'Z':
                zs[i].add(node)
        else:
            next_cycle[node] = current

    zs_sorted = sorted(zs.items())

    selected = {n for n in nodes if n[-1] == 'A'}

    t0 = time.monotonic_ns()
    full_cycle_count = 0
    while True:
        for in_cycle_count, node_set in zs_sorted:
            if selected <= node_set:
                steps = full_cycle_count * len(instructions) + in_cycle_count
                return steps

        selected = {next_cycle[n] for n in selected}
        full_cycle_count += 1

        if debug:
            total_steps = full_cycle_count * instructions_multiplier
            if total_steps % 1e6 == 0:
                t = time.monotonic_ns()
                total = (t-t0)
                avg = (t-t0) // total_steps
                print(f'avg = {avg}ns  |  total = {(total) / 1e9:.3f}s')


TEST_DATA = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

assert solve(TEST_DATA) == 6

print(solve(INPUT_DATA))  # 21165830176709 (took ~75 minutes in my computer)
