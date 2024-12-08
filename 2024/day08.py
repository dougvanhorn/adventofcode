#!/usr/bin/env python3

import collections
import itertools
import logging
import math
import pathlib


logging.basicConfig(level=logging.DEBUG, format='%(message)s')


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


def part_1(antenna_map):
    p('== Part 1 ==')
    antenna_map.part_1()


def part_2(antenna_map):
    p('== Part 2 ==')
    antenna_map.part_2()


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def point(self):
        # return a 2-tuple x, y.
        return (self.x, self.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))


class Antinodes:
    def __init__(self, cell_1, cell_2, map_size):
        # Contstruct with 2-tuples x y.
        self.cell_1 = cell_1
        self.cell_2 = cell_2
        self.delta_x = abs(cell_1.x - cell_2.x)
        self.delta_y = abs(cell_1.y - cell_2.y)
        self.map_size = map_size
        self.antinodes = []

    def part_1_nodes(self):
        HORIZONTAL = 0
        VERTICAL = math.inf
        # determine the slope.
        # We're not on standard cartsian.  Negative slope is ascending /, positive is descending \.
        cell_1 = self.cell_1
        cell_2 = self.cell_2

        if cell_1.x == cell_2.x:
            self.slope = VERTICAL
        else:
            self.slope = (cell_2.y - cell_1.y) / (cell_2.x - cell_1.x)

        # get antinodes.
        self.antinode_1 = None
        self.antinode_2 = None
        if self.slope == VERTICAL:
            top, bottom = sorted([cell_1, cell_2], key=lambda cell: cell.y)
            print(f'{self.slope} vertical top: {top}, right: {bottom}')
            self.antinode_1 = Cell(top.x, top.y - self.delta_y)
            self.antinode_2 = Cell(bottom.x, bottom.y + self.delta_y)

        elif self.slope == HORIZONTAL:
            left, right = sorted([cell_1, cell_2], key=lambda cell: cell.x)
            print(f'{self.slope} horizontal left: {left}, right: {right}')
            self.antinode_1 = Cell(left.x - self.delta_x, left.y)
            self.antinode_2 = Cell(right.x + self.delta_x, right.y)

        elif self.slope < 0:  # ascending: /
            lower_left, upper_right = sorted([cell_1, cell_2], key=lambda cell: cell.x)
            print(f'ascending left: {lower_left}, right: {upper_right}')
            self.antinode_1 = Cell(lower_left.x - self.delta_x, lower_left.y + self.delta_y)
            self.antinode_2 = Cell(upper_right.x + self.delta_x, upper_right.y - self.delta_y)

        elif self.slope > 0:  # descending: \
            upper_left, lower_right = sorted([cell_1, cell_2], key=lambda cell: cell.x)
            print(f'descending left: {upper_left}, right: {lower_right}')
            self.antinode_1 = Cell(upper_left.x - self.delta_x, upper_left.y - self.delta_y)
            self.antinode_2 = Cell(lower_right.x + self.delta_x, lower_right.y + self.delta_y)

        print(f'  delta_x: {self.delta_x}, delta_y: {self.delta_y}')
        print(f'  antinode_1: {self.antinode_1}')
        print(f'  antinode_2: {self.antinode_2}')
        self.antinodes = [self.antinode_1, self.antinode_2]

    def part_2_nodes(self):
        HORIZONTAL = 0
        VERTICAL = math.inf
        # determine the slope.
        # We're not on standard cartsian.  Negative slope is ascending /, positive is descending \.
        cell_1 = self.cell_1
        cell_2 = self.cell_2

        if cell_1.x == cell_2.x:
            self.slope = VERTICAL
        else:
            self.slope = (cell_2.y - cell_1.y) / (cell_2.x - cell_1.x)

        # get antinodes, build them until we're off the map.
        found_antinodes = []

        if self.slope == VERTICAL:
            top, bottom = sorted([cell_1, cell_2], key=lambda cell: cell.y)
            print(f'{self.slope} vertical top: {top}, right: {bottom}')

            # Include the towers, start at the y.
            up_y = range(top.y, 0, (-1 * self.delta_y))
            down_y = range(bottom.y, self.map_size, self.delta_y)
            for y in itertools.chain(up_y, down_y):
                found_antinodes.append(Cell(top.x, y))

        elif self.slope == HORIZONTAL:
            left, right = sorted([cell_1, cell_2], key=lambda cell: cell.x)
            print(f'{self.slope} horizontal left: {left}, right: {right}')

            # Include the towers, start at the y.
            left_x = range(left.x, 0, (-1 * self.delta_x))
            right_x = range(right.x, self.map_size, self.delta_x)
            for x in itertools.chain(left_x, right_x):
                found_antinodes.append(Cell(x, top.y))

        elif self.slope < 0:  # ascending: /
            lower_left, upper_right = sorted([cell_1, cell_2], key=lambda cell: cell.x)
            print(f'ASCENDING left: {lower_left}, right: {upper_right}, slope_x {self.delta_x} slope_y {self.delta_y}')

            left_x = range(lower_left.x, -1, (-1 * self.delta_x))
            left_y = range(lower_left.y, self.map_size, self.delta_y)
            left = zip(left_x, left_y)

            right_x = range(upper_right.x, self.map_size, self.delta_x)
            right_y = range(upper_right.y, -1, (-1 * self.delta_y))
            right = zip(right_x, right_y)

            for x, y in itertools.chain(left, right):
                found_antinodes.append(Cell(x, y))

        elif self.slope > 0:  # descending: \
            upper_left, lower_right = sorted([cell_1, cell_2], key=lambda cell: cell.x)
            print(f'DESCENDING left: {upper_left}, right: {lower_right}, slope_x {self.delta_x} slope_y {self.delta_y}')

            left_x = range(upper_left.x, -1, (-1 * self.delta_x))
            left_y = range(upper_left.y, -1, (-1 * self.delta_y))
            print(f'  left_x: {list(left_x)}, left_y: {list(left_y)}')
            left = zip(left_x, left_y)

            right_x = range(lower_right.x, self.map_size, self.delta_x)
            right_y = range(lower_right.y, self.map_size, self.delta_y)
            print(f'  left_x: {list(right_x)}, left_y: {list(right_y)}')
            right = zip(right_x, right_y)

            for x, y in itertools.chain(left, right):
                found_antinodes.append(Cell(x, y))

        print(f'  delta_x: {self.delta_x}, delta_y: {self.delta_y}')
        self.antinodes = found_antinodes
        print(f'  antinodes: {self.antinodes}')
        return self.antinodes

    def filter(self, map_size):
        # Return a set of antinodes that are within the map.
        antinodes = []
        antinodes = [
            antinode
            for antinode in self.antinodes
            if (0 <= antinode.x < map_size) and (0 <= antinode.y < map_size)
        ]
        return antinodes

    @property
    def distance(self):
        return 

class Frequency:
    def __init__(self, freq, map_size):
        self.freq = freq
        self.map_size = map_size
        self.antenna_list = []

    def __str__(self):
        return f'{self.freq}: {len(self.antenna_list)} antennas'

    @property
    def pairs(self):
        antenna_cells = [antenna.cell for antenna in self.antenna_list]
        return list(itertools.combinations(antenna_cells, 2))

    def add_antenna(self, antenna):
        self.antenna_list.append(antenna)

    def antinodes(self, map_size):
        # return a set of anitnodes as cells.
        pairs = self.pairs
        print(f'{len(pairs)}: {pairs}')
        found_antinodes = []
        for pair in pairs:
            antinodes = Antinodes(pair[0], pair[1], map_size)
            found_antinodes.extend(antinodes.filter(map_size))

        print(f'Found antinodes ({len(found_antinodes)}): {found_antinodes}')
        normalized_antinodes = set(found_antinodes)
        print(f'  Normalized ({len(normalized_antinodes)}): {normalized_antinodes}')
        return normalized_antinodes

    def antinodes_part_2(self, map_size):
        # return a set of anitnodes as cells.
        antenna_pairs = self.pairs
        print(f'{len(antenna_pairs)}: {antenna_pairs}')
        found_antinodes = []
        for pair in antenna_pairs:
            print('='*79)
            print('Getting antinodes for pair:', pair)
            antinodes = Antinodes(pair[0], pair[1], map_size)
            found_antinodes.extend(antinodes.part_2_nodes())
            print('-'*79)

        return found_antinodes



class Antenna:
    def __init__(self, cell, freq):
        self.cell = cell
        self.freq = freq

    def __str__(self):
        return f'{self.cell}:{self.freq}'


class AntennaMap:
    def __init__(self, data):
        self.map_size = len(data)
        self.data = data
        self.map = []
        self.frequencies = {}

        # process input data.
        for y, row in enumerate(data):
            current_row = []
            self.map.append(current_row)
            for x, value in enumerate(row):
                # Skip empty cells.
                if value == '.':
                    continue

                cell = Cell(x, y)
                antenna = Antenna(cell, value)
                freq = self.frequencies.setdefault(value, Frequency(value, self.map_size))
                freq.add_antenna(antenna)

        print('Frequencies:')
        frequency_keys = list(self.frequencies.keys())
        frequency_keys.sort()
        for key in frequency_keys:
            print(f'  {self.frequencies[key]}')

    def part_1(self):
        print('Antinodes:')
        all_antinodes = []
        for freq in self.frequencies.values():
            antinodes = freq.antinodes(self.map_size)
            print(f'Found antinodes for {freq}: {antinodes}')
            all_antinodes.extend(antinodes)

        # normalize antinodes.
        normalized = {antinode.point for antinode in all_antinodes}
        print(f'Answer: {len(normalized)}')
        sorted_antinodes = sorted(list(normalized), key=lambda cell: (cell[1], cell[0]))
        print(sorted_antinodes)

    def part_2(self):
        all_antinodes = []
        for freq in self.frequencies.values():
            print('='*79)
            print(f'Getting antinodes for: {freq}')
            print('-'*79)
            antinodes = freq.antinodes_part_2(self.map_size)
            print(f'Found antinodes for {freq}: {antinodes}')
            all_antinodes.extend(antinodes)
            print('-'*79)

        # normalize antinodes.
        normalized = {antinode.point for antinode in all_antinodes}
        sorted_antinodes = sorted(list(normalized), key=lambda cell: (cell[1], cell[0]))
        # print(sorted_antinodes)
        print(f'Answer: {len(normalized)}')


def main(data):
    antenna_map = AntennaMap(data)
    # part_1(antenna_map)
    antenna_map.part_2()


if __name__ == '__main__':
    data = load_data()
    _data = [
        '............',
        '........0...',
        '.....0......',
        '.......0....',
        '....0.......',
        '......A.....',
        '............',
        '............',
        '........A...',
        '.........A..',
        '............',
        '............',
    ]
    main(data)
