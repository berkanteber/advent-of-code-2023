from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def _sort(string: str, *, reverse: bool = False) -> str:
    return ''.join(sorted(string, key=lambda ch: {'O': 0, '.': 1}[ch], reverse=reverse))


def _tilt(col: str, *, reverse: bool = False) -> str:
    parts = []
    for part in col.split('#'):
        parts.append(_sort(part, reverse=reverse))
    return '#'.join(parts)


def _change(rows_or_cols: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(''.join(lst) for lst in zip(*rows_or_cols))


def _cycle(cols: tuple[str, ...]) -> tuple[str, ...]:
    cols = tuple(_tilt(col) for col in cols)
    rows = _change(cols)

    rows = tuple(_tilt(row) for row in rows)
    cols = _change(rows)

    cols = tuple(_tilt(col, reverse=True) for col in cols)
    rows = _change(cols)

    rows = tuple(_tilt(row, reverse=True) for row in rows)
    cols = _change(rows)

    return tuple(cols)


def solve(data: str, *, debug: bool = False) -> int:
    cols = _change(tuple(data.splitlines()))

    prevs = {cols: 0}
    i = 1
    while i <= 1_000_000_000:
        if debug and i % 1_000_000 == 0:
            print(f'{i:,d}')

        cols = _cycle(cols)

        if (prev := prevs.get(cols)) is not None:
            diff = i - prev
            i += (1_000_000_000 - i) // diff * diff + 1
            if debug:
                print(f'jumping to: {i:,d}')
            continue

        prevs[cols] = i
        i += 1

    total = 0
    length = len(cols[0])
    for col in cols:
        for i, ch in enumerate(col):
            if ch == 'O':
                total += length - i

    return total


TEST_DATA = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

TEST_CYCLE_1 = """\
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
"""

TEST_CYCLE_2 = """\
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O
"""

TEST_CYCLE_3 = """\
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
"""

cycle_0 = _change(tuple(TEST_DATA.splitlines()))
cycle_1 = _cycle(cycle_0)
cycle_2 = _cycle(cycle_1)
cycle_3 = _cycle(cycle_2)

assert cycle_1 == _change(tuple(TEST_CYCLE_1.splitlines()))
assert cycle_2 == _change(tuple(TEST_CYCLE_2.splitlines()))
assert cycle_3 == _change(tuple(TEST_CYCLE_3.splitlines()))

assert solve(TEST_DATA) == 64

print(solve(INPUT_DATA))  # 108404
