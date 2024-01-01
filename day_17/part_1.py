from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


MAX = 10 ** 10


def solve(data: str) -> int:
    diagram = {
        (i, j): int(num_s)
        for i, row in enumerate(data.splitlines())
        for j, num_s in enumerate(row)
    }

    seen = {}
    nexts: dict[tuple[tuple[int, int], str], int] = {
        ((0, 1), 'r'): diagram[0, 1],
        ((1, 0), 'd'): diagram[1, 0],
    }
    while nexts:
        current = min(nexts, key=nexts.__getitem__)
        cost = nexts.pop(current)

        # print(current, cost)
        seen[current] = cost

        (row, col), dirs = current

        rrr = (row, col+1)
        lll = (row, col-1)
        uuu = (row-1, col)
        ddd = (row+1, col)

        possible_nexts: set[tuple[tuple[int, int], str]] = set()
        if dirs.endswith(('r', 'u', 'd')):
            possible_nexts.add((rrr, dirs + 'r'))
        if dirs.endswith(('l', 'u', 'd')):
            possible_nexts.add((lll, dirs + 'l'))
        if dirs.endswith(('r', 'l', 'u')):
            possible_nexts.add((uuu, dirs + 'u'))
        if dirs.endswith(('r', 'l', 'd')):
            possible_nexts.add((ddd, dirs + 'd'))

        for ppos, pdirs in possible_nexts:
            pcost = diagram.get(ppos)
            if pcost is None:
                continue

            if len(set(pdirs)) == 2:
                pdirs = pdirs[-1]

            if pdirs in ('rrrr', 'llll', 'uuuu', 'dddd'):
                continue

            if (ppos, pdirs) in seen:
                continue

            prev = nexts.get((ppos, pdirs), MAX)
            nexts[ppos, pdirs] = min(cost + pcost, prev)

    max_row = max(r for r, _ in diagram.keys())
    max_col = max(c for _, c in diagram.keys())

    return min(scost for (spos, _), scost in seen.items() if spos == (max_row, max_col))


TEST_DATA = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

assert solve(TEST_DATA) == 102

print(solve(INPUT_DATA))  # 817
