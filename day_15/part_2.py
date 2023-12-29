from __future__ import annotations

import os


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def _hash(label: str) -> int:
    current = 0
    for ch in label:
        current += ord(ch)
        current = current * 17 % 256

    return current


def solve(data: str) -> int:
    steps = data.strip().split(',')

    boxes: dict[int, dict[str, int]] = {i: {} for i in range(256)}
    for step in steps:
        if '=' in step:
            label, focal_length_s = step.split('=')
            box = _hash(label)
            # dict is already ordered & updates don't change order
            boxes[box][label] = int(focal_length_s)
        elif '-' in step:
            label = step[:-1]
            box = _hash(label)
            boxes[box].pop(label, None)
        else:
            raise AssertionError

    total = 0
    for box, d in boxes.items():
        for i, focal_length in enumerate(d.values(), 1):
            total += (box + 1) * i * focal_length

    return total


TEST_DATA = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

assert solve(TEST_DATA) == 145

print(solve(INPUT_DATA))  # 286104
