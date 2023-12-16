from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def _adj(ch: str, pos: tuple[int, int]) -> list[tuple[int, int]]:
    r, c = pos

    match ch:
        case '|':
            return [(r+1, c), (r-1, c)]
        case '-':
            return [(r, c+1), (r, c-1)]
        case 'L':
            return [(r-1, c), (r, c+1)]
        case 'J':
            return [(r, c-1), (r-1, c)]
        case '7':
            return [(r, c-1), (r+1, c)]
        case 'F':
            return [(r, c+1), (r+1, c)]
        case 'S':
            return [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        case _:
            return []


def _can_connect(
    diagram: list[list[str]],
    pos1: tuple[int, int],
    pos2: tuple[int, int],
) -> bool:
    r1, c1 = pos1
    ch1 = diagram[r1][c1]

    r2, c2 = pos2
    ch2 = diagram[r2][c2]

    return pos1 in _adj(ch2, pos2) and pos2 in _adj(ch1, pos1)


def _nexts(diagram: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    r, c = pos

    len_row = len(diagram)
    len_col = len(diagram[0])

    return [
        (nr, nc) for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        if 0 <= nr < len_row and 0 <= nc < len_col
        and _can_connect(diagram, pos, (nr, nc))
    ]


def solve(data: str, *, debug: bool = False) -> int:
    diagram = [[ch for ch in line] for line in data.splitlines()]

    for row, line in enumerate(diagram):
        for col, cell in enumerate(line):
            if cell == 'S':
                start = row, col

    nexts = [[start, n] for n in _nexts(diagram, start)]
    while nexts:
        route = nexts.pop()
        last = route[-1]

        lnexts = _nexts(diagram, last)
        if len(route) != 2 and start in lnexts:
            break

        nexts += [route + [ln] for ln in lnexts if ln not in route]

    # replace `S` with correct one
    last = route[-1]
    second = route[1]
    ch, = (
        ch for ch in '|-LJ7F'
        if last in _adj(ch, start) and second in _adj(ch, start)
    )
    sr, sc = start
    diagram[sr][sc] = ch

    route_set = set(route)

    min_row, max_row = min(r for r, _ in route), max(r for r, _ in route)
    min_col, max_col = min(c for _, c in route), max(c for _, c in route)

    # assume there is `|` or `-` in relevant boundaries
    for i, (r, c) in enumerate(route):
        if diagram[r][c] == '-' and r in (min_row, max_row):
            route = route[i:] + route[:i]
            inside_direction = 'down' if r == min_row else 'up'
            break

        if diagram[r][c] == '|' and c in (min_col, max_col):
            route = route[i:] + route[:i]
            inside_direction = 'right' if c == min_col else 'left'
            break

    # find dots inside adjacent to the route
    in_dots = set()
    for r, c in route:
        ch = diagram[r][c]

        match [ch, inside_direction]:
            case ['-', 'down'] | ['-', 'up']:
                new_inside_direction = inside_direction
            case ['|', 'left'] | ['|', 'right']:
                new_inside_direction = inside_direction
            case ['F', d] | ['J', d]:
                new_inside_direction = {
                    'right': 'down',
                    'left': 'up',
                    'down': 'right',
                    'up': 'left',
                }[d]
            case ['L', d] | ['7', d]:
                new_inside_direction = {
                    'right': 'up',
                    'left': 'down',
                    'down': 'left',
                    'up': 'right',
                }[d]
            case ch, d:
                raise AssertionError(f'{ch=} {d=}')

        dots = {
            {'up': (r-1, c), 'down': (r+1, c), 'left': (r, c-1), 'right': (r, c+1)}[d]
            for d in (inside_direction, new_inside_direction)
        }
        for dot in dots:
            dr, dc = dot
            if (
                min_row <= dr <= max_row and min_col <= dc <= max_col
                and dot not in route_set
            ):
                in_dots.add(dot)

        inside_direction = new_inside_direction

    # find all reachable dots from dots inside adjacent to the route
    dots = {d for d in in_dots}
    inside = set()
    while dots:
        dot_group = {dots.pop()}
        len_dot_group = 1
        while True:
            dot_group = set.union(
                *[
                    {
                        (r, c) for r, c in
                        ((dr, dc), (dr-1, dc), (dr+1, dc), (dr, dc-1), (dr, dc+1))
                        if (
                            min_row <= r <= max_row and min_col <= c <= max_col
                            and (r, c) not in route_set
                        )
                    }
                    for dr, dc in dot_group
                ],
            )
            if len(dot_group) == len_dot_group:
                break

            len_dot_group = len(dot_group)

        dots -= dot_group

        if dot_group & in_dots:
            inside |= dot_group

    if debug:
        for row, line in enumerate(diagram):
            for col, cell in enumerate(line):
                if (row, col) in route_set:
                    print(cell, end='')
                elif (row, col) in inside:
                    print('X', end='')
                else:
                    print(' ', end='')
            print()

    return len(inside)


TEST_DATA_1 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

TEST_DATA_2 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

TEST_DATA_3 = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

assert solve(TEST_DATA_1) == 4
assert solve(TEST_DATA_2) == 8
assert solve(TEST_DATA_3) == 10

print(solve(INPUT_DATA))  # 273
