from __future__ import annotations

import os
from collections import Counter
from dataclasses import dataclass


INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT_PATH) as f:
    INPUT_DATA = f.read()


@dataclass
class Hand:
    cards: str
    bid: int

    @property
    def score(self) -> tuple[int, ...]:
        sums = [count for _, count in Counter(self.cards).most_common()]
        if sums == [5]:
            type_score = 7
        elif sums == [4, 1]:
            type_score = 6
        elif sums == [3, 2]:
            type_score = 5
        elif sums == [3, 1, 1]:
            type_score = 4
        elif sums == [2, 2, 1]:
            type_score = 3
        elif sums == [2, 1, 1, 1]:
            type_score = 2
        else:
            type_score = 1

        card_scores = {
            c: -i for i, c
            in enumerate(
                ('A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'),
            )
        }
        hand_score = [card_scores[c] for c in self.cards]

        return (type_score, *hand_score)


def solve(data: str) -> int:
    hands = []
    for line in data.splitlines():
        cards, bid_s = line.split()
        hands.append(Hand(cards=cards, bid=int(bid_s)))

    total = 0
    for rank, hand in enumerate(sorted(hands, key=lambda h: h.score), 1):
        total += rank * hand.bid

    return total


TEST_DATA = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

assert solve(TEST_DATA) == 6440

print(solve(INPUT_DATA))  # 250347426
