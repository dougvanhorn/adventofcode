#!/usr/bin/env python

import collections
import logging
import math
import pathlib
import unittest


logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class DialTest(unittest.TestCase):
    def test_right(self):
        dial = Dial(50)

        dial.turn_dial('R', 30)
        self.assertEqual(dial.position, 80)
        self.assertEqual(dial.zeros, 0)

        dial.turn_dial('R', 25)
        self.assertEqual(dial.position, 5)
        self.assertEqual(dial.zeros, 1)

        dial.turn_dial('R', 95)
        self.assertEqual(dial.position, 0)
        self.assertEqual(dial.zeros, 2)

        dial.turn_dial('R', 50)
        self.assertEqual(dial.position, 50)
        self.assertEqual(dial.zeros, 2)

        dial.turn_dial('R', 479)
        self.assertEqual(dial.position, 29)
        # 4 full, plus 1 crossing, plus 2 already visited.
        self.assertEqual(dial.zeros, 7) 

        dial.turn_dial('R', 300)
        self.assertEqual(dial.position, 29)
        # 4 full, plus 1 crossing, plus 2 already visited.
        self.assertEqual(dial.zeros, 10) 

        dial.turn_dial('R', 71)
        self.assertEqual(dial.position, 0)
        # 4 full, plus 1 crossing, plus 2 already visited.
        self.assertEqual(dial.zeros, 11) 

        dial.turn_dial('R', 200)
        self.assertEqual(dial.position, 0)
        # 4 full, plus 1 crossing, plus 2 already visited.
        self.assertEqual(dial.zeros, 13) 

    def test_left(self):
        dial = Dial(50)

        dial.turn_dial('L', 30)
        self.assertEqual(dial.position, 20)
        self.assertEqual(dial.zeros, 0)

        dial.turn_dial('L', 25)
        self.assertEqual(dial.position, 95)
        self.assertEqual(dial.zeros, 1)

        dial.turn_dial('L', 95)
        self.assertEqual(dial.position, 0)
        self.assertEqual(dial.zeros, 2)

        dial.turn_dial('L', 50)
        self.assertEqual(dial.position, 50)
        self.assertEqual(dial.zeros, 2)

        dial.turn_dial('L', 479)
        self.assertEqual(dial.position, 71)
        # 4 full, plus 1 crossing, plus 2 already visited.
        self.assertEqual(dial.zeros, 7) 


class Dial:
    def __init__(self, position=50):
        self.position = position
        # The number of times we tick to 0.
        self.zeros = 0

    def turn(self, direction):
        if direction == 'L':
            self.position -= 1
            if self.position < 0:
                self.position = 99
        elif direction == 'R':
            self.position += 1
            if self.position > 99:
                self.position = 0
        else:
            raise ValueError(f'Invalid direction: {direction}')

    def turn_dial(self, direction, full_ticks):
        # Reduce ticks to full rotations + modulo.
        full_rotations, remaining_ticks = divmod(full_ticks, 100)

        if self.position < 0 or self.position > 100:
            raise ValueError(f'Invalid dial position: {self.position}')

        # p(f'Starting at: {self.position}, Zeros: {self.zeros}.')
        # p(f'  Moving {direction} by {full_ticks}.')
        # p(f'  Zeros from full rotations: {full_rotations}')

        start_position = self.position

        if remaining_ticks == 0:
            # p('  No remaining ticks after full rotations.')
            self.zeros += full_rotations
            return

        # Apply the remaining ticks in the given direction.
        if direction == 'L':
            zeros = 0
            # Moving left, we subtract the remainder.
            end_position = self.position - remaining_ticks
            # p(f'  End position after left turn: {end_position}')
            # If we land on zero, count it.
            if end_position == 0:
                zeros += 1
            elif end_position < 0:
                end_position += 100 # Wrap around.
                if start_position != 0:
                    # We we crossed zero (didn't start there), count it.
                    zeros += 1
            # p(f'  End position: {end_position}')
            # p(f'  Zeros after left turn: {zeros}')
            self.zeros += (full_rotations + zeros)
            self.position = end_position

        elif direction == 'R':
            zeros = 0
            end_position = self.position + remaining_ticks
            # p(f'  End position after right turn: {end_position}')
            # If we're >= 100, count the zero.
            if end_position == 100:
                zeros += 1
                end_position = 0  # Set our position to 0.
            elif end_position > 100:
                zeros += 1
                end_position -= 100
            # p(f'  End position: {end_position}')
            # p(f'  Zeros after right turn: {self.zeros}')
            self.zeros += (full_rotations + zeros)
            self.position = end_position
            return

        else:
            raise ValueError(f'Invalid direction: {direction}')

    def is_zero(self):
        return self.position == 0


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
    dial = Dial()
    zeros = 0
    for row in data:
        direction, clicks = row[0], int(row[1:])
        dial.turn_dial(direction, clicks)
        # p(f'Dial turned {row}, now at position {dial.position}')
        if dial.is_zero():
            zeros += 1
            # p('Dial is at zero!')

    print(f'Dial hit zero {zeros} times.')


def part_2(data):
    p('== Part 2 ==')
    dial = Dial()
    for row in data:
        direction, ticks = row[0], int(row[1:])
        dial.turn_dial(direction, ticks)

    print(f'Dial hit zero {dial.zeros} times.')


def part_2_naive(data):
    p('== Part 2 Naive ==')
    dial = Dial()
    total = 0
    for row in data:
        direction, ticks = row[0], int(row[1:])
        for _ in range(ticks):
            dial.turn(direction)
            if dial.is_zero():
                total += 1

    print(f'Dial hit zero {total} times.')


def main(data):
    _data = [
        'L68',
        'L30',
        'R48',
        'L5',
        'R60',
        'L55',
        'L1',
        'L99',
        'R14',
        'L82',
    ]
    part_1(data)
    part_2(data)
    # part_2_naive(_data)
    # part_2_naive(data)


if __name__ == '__main__':
    data = load_data()
    main(data)
