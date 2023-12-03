#!/usr/bin/env python3

import collections
import math
import logging
import pathlib
import re

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def debug(message):
    log = logging.getLogger('aoc')
    log.debug(message)


class Schematic:
    def __init__(self, data):
        self.data = data
        self.width = len(data[0])
        self.height = len(data)

        part_pattern = re.compile('\d+')
        self.matches = [(i, list(part_pattern.finditer(row))) for i, row in enumerate(data)]

        self.gears = []
        for row, line in enumerate(data):
            for col, char in enumerate(line):
                if char == '*':
                    self.gears.append((row, col))

    def print(self):
        for row in self.matches:
            print(row)

        for row_number, matches in self.matches:
            for match in matches:
                neighbors = self.neighbors(row_number, match)
                print(match)
                print(neighbors)
                print()

    def neighbors(self, row_number, match):
        """Return a list of coords to check."""
        left, right = match.span()

        cells = []
        left_right_range = list(range(max(0, left-1), min(self.width-1, right+1)))
        print(f'match: {match.group()}, row number: {row_number}, ({left}, {right}), range {left_right_range}')
        # Above
        if row_number > 0:
            cells.extend(
                [
                    (row_number-1, column)
                    for column in left_right_range
                ]
            )

        if left > 0:
            cells.append((row_number, left-1))
        if right < (self.width-1):
            cells.append((row_number, right))

        # Below
        if row_number < self.height-1:
            cells.extend(
                [
                    (row_number+1, column)
                    for column in left_right_range
                ]
            )

        return cells

    def part1(self):
        self.print()
        parts = []
        for row_number, matches in self.matches:
            for match in matches:
                neighbors = self.neighbors(row_number, match)
                for row, col in neighbors:
                    cell = self.data[row][col]
                    #print(f'match: {match.group()}, row number: {row_number}, ({row}, {col}), cell: {cell}')
                    if cell not in '0123456789.':
                        parts.append(match)
                        break

        #print(parts)
        total = sum([int(m.group()) for m in parts])
        print('Answer', total)

    def part2(self):
        #print(self.gears)

        gears = collections.defaultdict(list)

        for row_number, matches in self.matches:
            for match in matches:
                neighbors = self.neighbors(row_number, match)
                for row, col in neighbors:
                    cell = self.data[row][col]
                    # If the part is next to a gear, add it to the gear's list.
                    if cell == '*':
                        gears[(row, col)].append(match)

        total = 0
        print(gears)
        for gear, parts in gears.items():
            if len(parts) == 2:
                total += (int(parts[0].group()) * int(parts[1].group()))

        print('Answer:', total)


def part_1(data):
    debug('== Part 1 ==')
    _data = [
        '467..114..',
        '...*......',
        '..35..633.',
        '......#...',
        '617*......',
        '.....+.58.',
        '..592.....',
        '......755.',
        '...$.*....',
        '.664.598..',
    ]
    schematic = Schematic(data)
    schematic.part1()


def part_2(data):
    _data = [
        '467..114..',
        '...*......',
        '..35..633.',
        '......#...',
        '617*......',
        '.....+.58.',
        '..592.....',
        '......755.',
        '...$.*....',
        '.664.598..',
    ]
    debug('== Part 2 ==')

    schematic = Schematic(data)
    schematic.part2()


def main(data):
    #part_1(data)
    #print()
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)
