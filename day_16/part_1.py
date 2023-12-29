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

    energized = set()
    seen = set()
    beams = {(0, 0, 'r')}
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

    return len(energized)


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

assert solve(TEST_DATA) == 46

print(solve(INPUT_DATA))  # 8116
