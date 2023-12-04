#!/usr/bin/env python3

import collections
import math
import logging
import pathlib

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class Deck:
    def __init__(self, data):
        self.original_cards = [Card(i, row) for i, row in enumerate(data)]

        self.cards = {
            card: 1
            for card in self.original_cards
        }

        for i, card in enumerate(self.original_cards):
            count = card.winner_count()

            next_card_pos = i + 1
            current_card_count = self.cards[card]
            for win_card in self.original_cards[next_card_pos:next_card_pos+count]:
                self.cards[win_card] += current_card_count

        for card, count in self.cards.items():
            print(card, 'Winners', count)
        print()

    def card_total(self):
        return sum(count for count in self.cards.values())


class Card:
    def __init__(self, number, s):
        self.number = number
        self.name, card_numbers = s.split(': ')
        winning_numbers, card_numbers = card_numbers.split(' | ')

        self.winners = winning_numbers.split()
        self.winners_set = set(self.winners)

        self.cards = card_numbers.split()
        self.cards_set = set(self.cards)

        self._value = None

    def __str__(self):
        winners = ' '.join(self.winners)
        cards = ' '.join(self.cards)
        s = f'[{self.number}] {self.name}: {winners} | {cards}'
        return s

    def __repr__(self):
        return self.__str__()

    def value(self):
        found = [card for card in self.cards_set if card in self.winners_set]
        #print(f'Found {found} matching cards.')

        if not found:
            return 0
        self._value = int(math.pow(2, len(found)-1))
        return self._value

    def winner_count(self):
        found = [card for card in self.cards_set if card in self.winners_set]
        return len(found)


def debug(message):
    log = logging.getLogger('aoc')
    log.debug(message)


def part_1(data):
    debug('== Part 1 ==')
    cards = [Card(i, s) for i, s in enumerate(data)]
    total = sum(card.value() for card in cards)
    print('Answer', total)


def part_2(data):
    debug('== Part 2 ==')
    deck = Deck(data)
    total = deck.card_total()
    print('Answer', total)


def main(data):
    _data = [
        'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
        'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
        'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
        'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
        'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
        'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11',
    ]
    #part_1(data)
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)
