from __future__ import annotations

import os
import re


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


def solve(data: str) -> int:
    pattern = re.compile(r'Card\s+(?P<card>\d+): (?P<wins>[\d ]+) \| (?P<nums>[\d ]+)')

    cards = {}
    for line in data.splitlines():
        m = pattern.fullmatch(line)
        assert m is not None

        card = int(m['card'])
        wins = set(map(int, m['wins'].split()))
        nums = list(map(int, m['nums'].split()))

        won = sum(1 for num in nums if num in wins)

        cards[card] = won

    card = max(cards.keys())
    while card:
        next_card = card + 1
        next_cards = range(next_card, next_card + cards[card])

        cards[card] = 1 + sum(cards[nc] for nc in next_cards)

        card -= 1

    total = sum(cards.values())

    return total


TEST_DATA = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53  4
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19  2
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1  2
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83  1
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36  0
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11  0
"""

assert solve(TEST_DATA) == 30

print(solve(INPUT_DATA))  # 13768818
