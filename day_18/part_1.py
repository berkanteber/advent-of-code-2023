from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def solve(data: str) -> int:
    current = (0, 0)
    perimeter = {current}
    insides = set()
    for line in data.splitlines():
        d, num_s, _ = line.split()
        for _ in range(int(num_s)):
            r, c = current
            match d:
                case 'R':
                    current = (r, c+1)
                    insides.add((r+1, c+1))
                case 'L':
                    current = (r, c-1)
                    insides.add((r-1, c-1))
                case 'U':
                    current = (r-1, c)
                    insides.add((r-1, c+1))
                case 'D':
                    current = (r+1, c)
                    insides.add((r+1, c-1))

            perimeter.add(current)

    insides -= perimeter
    all_insides = set()
    while insides:
        dot_group = {insides.pop()}
        while True:
            new_dot_group = set()
            for dot in dot_group:
                new_dot_group.add(dot)
                dr, dc = dot
                for new_dot in ((dr+1, dc), (dr-1, dc), (dr, dc+1), (dr, dc-1)):
                    if new_dot not in perimeter:
                        new_dot_group.add(new_dot)

            if new_dot_group == dot_group:
                break

            dot_group = new_dot_group

        insides -= dot_group
        all_insides |= dot_group

    return len(all_insides) + len(perimeter)


TEST_DATA = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

assert solve(TEST_DATA) == 62

print(solve(INPUT_DATA))  # 58550
