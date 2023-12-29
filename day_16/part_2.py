from __future__ import annotations

import os
import textwrap


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def solve(data: str) -> int:
    diagram = {}
    for i, row in enumerate(data.splitlines()):
        for j, ch in enumerate(row):
            diagram[i, j] = ch

    len_row = max(r for r, _ in diagram.keys()) + 1
    len_col = max(c for _, c in diagram.keys()) + 1

    confs = []
    confs.extend([(0, c, 'd') for c in range(len_col)])
    confs.extend([(len_row - 1, c, 'u') for c in range(len_col)])
    confs.extend([(r, 0, 'r') for r in range(len_row)])
    confs.extend([(r, len_col - 1, 'l') for r in range(len_row)])

    totals = {}
    for conf in confs:
        energized = set()
        seen = set()
        beams = {conf}
        while beams:
            beam = beams.pop()

            if beam in seen:
                continue
            else:
                seen.add(beam)

            pos = beam[:-1]
            direction = beam[-1]
            try:
                current = diagram[pos]
            except KeyError:
                continue
            else:
                energized.add(pos)

            r, c = pos
            beams |= {
                ('.', 'r'): {(r, c+1, direction)},
                ('.', 'l'): {(r, c-1, direction)},
                ('.', 'u'): {(r-1, c, direction)},
                ('.', 'd'): {(r+1, c, direction)},
                ('|', 'u'): {(r-1, c, direction)},
                ('|', 'd'): {(r+1, c, direction)},
                ('-', 'r'): {(r, c+1, direction)},
                ('-', 'l'): {(r, c-1, direction)},
                ('|', 'r'): {(r-1, c, 'u'), (r+1, c, 'd')},
                ('|', 'l'): {(r-1, c, 'u'), (r+1, c, 'd')},
                ('-', 'u'): {(r, c-1, 'l'), (r, c+1, 'r')},
                ('-', 'd'): {(r, c-1, 'l'), (r, c+1, 'r')},
                ('/', 'u'): {(r, c+1, 'r')},
                ('/', 'd'): {(r, c-1, 'l')},
                ('/', 'r'): {(r-1, c, 'u')},
                ('/', 'l'): {(r+1, c, 'd')},
                ('\\', 'u'): {(r, c-1, 'l')},
                ('\\', 'd'): {(r, c+1, 'r')},
                ('\\', 'r'): {(r+1, c, 'd')},
                ('\\', 'l'): {(r-1, c, 'u')},
            }[current, direction]

        totals[conf] = len(energized)

    return max(totals.values())


TEST_DATA = textwrap.dedent(
    r"""
        .|...\....
        |.-.\.....
        .....|-...
        ........|.
        ..........
        .........\
        ..../.\\..
        .-.-/..|..
        .|....-|.\
        ..//.|....
    """,
).strip('\n')

assert solve(TEST_DATA) == 51

print(solve(INPUT_DATA))  # 8383
