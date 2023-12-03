from __future__ import annotations

import os
import re


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def _adjacent(pos: tuple[int, int, int], board: list[list[str]]) -> bool:
    lineno, start, end = pos
    len_row = len(board)
    len_col = len(board[0])

    adj = set.union(
        {(row, start - 1) for row in (lineno - 1, lineno, lineno + 1)},  # left
        {(row, end) for row in (lineno - 1, lineno, lineno + 1)},        # right
        {(lineno - 1, col) for col in range(start, end)},                # up
        {(lineno + 1, col) for col in range(start, end)},                # down
    )
    for row, col in adj:
        if not (0 <= row < len_row and 0 <= col < len_col):
            continue

        if board[row][col] != '.':
            return True

    return False


def solve(data: str) -> int:
    pattern = re.compile(r'(?P<num>\d+)')

    nums = []
    board = []
    for lineno, line in enumerate(data.splitlines()):
        for m in pattern.finditer(line):
            start, end = m.span()
            pos = (lineno, start, end)
            num = int(m['num'])
            nums.append((pos, num))

        board.append(list(line))

    total = 0
    for pos, num in nums:
        if _adjacent(pos, board):
            total += num

    return total


TEST_DATA = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

assert solve(TEST_DATA) == 4361

print(solve(INPUT_DATA))  # 527446
