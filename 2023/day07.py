#!/usr/bin/env python3

import collections
import math
import logging
import operator
import pathlib

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

FIVE = 7
FOUR = 6
FULL = 5
THREE = 4
TWO = 3
ONE = 2
HIGH = 1
CARD_VALUES = {
    'A': 14,
    'K': 13,
    'Q': 12,
    #'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
    'J': 1
}


class Hand:
    def __init__(self, s):
        parts = s.split()
        self.hand = parts[0]
        self.bid = int(parts[1])
        self.cards = [c for c in self.hand]

        # Determine hand type

        self.hand_type = None
        #self.set_part1_hand()
        self.set_part2_hand()

        if self.hand_type is None:
            raise Exception(self.hand)

        self.hand_value = tuple([self.hand_type] + [CARD_VALUES[card] for card in self.cards])


    def set_part1_hand(self):
        card_groups = collections.defaultdict(int)
        for card in self.hand:
            card_groups[card] += 1

        card_counts = set(card_groups.values())
        card_values = sorted(list(card_groups.values()), reverse=True)

        if card_counts == {5}:
            self.hand_type = FIVE

        elif card_counts == {4, 1}:
            self.hand_type = FOUR

        elif card_counts == {3, 2}:
            self.hand_type = FULL

        elif card_counts == {3, 1}:
            self.hand_type = THREE

        elif card_values == [2, 2, 1]:
            self.hand_type = TWO

        elif card_values == [2, 1, 1, 1]:
            self.hand_type = ONE

        elif card_values == [1, 1, 1, 1, 1]:
            self.hand_type = HIGH

        else:
            print('unknown hand:', self.hand)
            print('  ', card_counts)
            print('  ', card_values)
            raise Exception()

    def set_part2_hand(self):
        cards = [c for c in self.cards if c != 'J']
        card_count = len(cards)
        jokers = [c for c in self.cards if c == 'J']
        joker_count = len(jokers)

        card_groups = collections.defaultdict(int)
        # {'A': 1, 'K': 3}
        for card in cards:
            card_groups[card] += 1
        # {1, 3}
        card_set = set(card_groups.values())
        # [3, 1]
        card_counts = sorted(list(card_groups.values()), reverse=True)

        if self.hand == 'JJJJJ':
            print('all jokers')

        if joker_count == 0:
            self.set_part1_hand()
            return

        # only deal with joker hands
        if joker_count == 5:
            self.hand_type = FIVE
            return

        if joker_count == 4:
            self.hand_type = FIVE
            return

        if joker_count == 3:
            if card_set == {2}:
                self.hand_type = FIVE
                return
            if card_set == {1}:  # 1, 1
                self.hand_type = FOUR
                return

        if joker_count == 2:
            if card_set == {3}:
                self.hand_type = FIVE
                return

            if card_set == {2, 1}:
                self.hand_type = FOUR
                return

            if card_set == {1}:  # 1, 1, 1
                self.hand_type = THREE
                return

        if joker_count == 1:
            if card_set == {4}:
                self.hand_type = FIVE
                return

            if card_set == {3, 1}:
                self.hand_type = FOUR
                return

            if card_set == {2, 2}:
                self.hand_type = FULL
                return

            if card_set == {2, 1}:  # 2, 1, 1
                self.hand_type = THREE
                return

            if card_set == {1}:  # 1, 1, 1, 1
                self.hand_type = ONE
                return

        print('unknown hand:', self.hand)
        print('  cards', cards, 'count', card_count)
        print('  jokers', jokers, 'count', joker_count)
        print('  card_counts', card_counts)
        print('  card_set', card_set)
        raise Exception('unknow hand')

    def __str__(self):
        s = f'{self.cards} {self.bid}:   {self.hand_value}'
        return s

    def __repr__(self):
        return str(self)


def load_data():
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]
    return data


def p(message):
    log = logging.getLogger('aoc')
    log.debug(message)


def part_1(data):
    p('== Part 1 ==')
    hands = [Hand(row) for row in data]
    # print('Original')
    # for hand in hands:
    #     print(hand)

    # hands.sort(key=operator.attrgetter('hand_value'), reverse=True)

    # print('-'*79)
    # print('Sorted')
    # for hand in hands:
    #     print(hand)

    hands.sort(key=operator.attrgetter('hand_value'))
    answer = 0
    for rank, hand in enumerate(hands, start=1):
        answer += (rank * hand.bid)

    print('Answer', answer)


def part_2(data):
    p('== Part 2 ==')
    hands = [Hand(row) for row in data]
    # print('Original')
    # for hand in hands:
    #     print(hand)

    # hands.sort(key=operator.attrgetter('hand_value'), reverse=True)

    # print('-'*79)
    # print('Sorted')
    # for hand in hands:
    #     print(hand)

    hands.sort(key=operator.attrgetter('hand_value'))
    answer = 0
    for rank, hand in enumerate(hands, start=1):
        answer += (rank * hand.bid)

    print('Answer', answer)


def main(data):
    _data = [
        '32T3K 765',
        'T55J5 684',
        'KK677 28',
        'KTJJT 220',
        'QQQJA 483',
    ]
    #part_1(data)
    part_2(data)


if __name__ == '__main__':
    data = load_data()
    main(data)
