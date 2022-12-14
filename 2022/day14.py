#!/usr/bin/env python3

import collections
from dataclasses import dataclass
import itertools
import math
import logging
import pathlib
import time


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
def debug(message):
    log = logging.getLogger('aoc')
    log.debug(message)


class Cell:
    @classmethod
    def from_string(cls, data):
        # Constructor from string.
        x, y = data.split(',')
        x = int(x)
        y = int(y)
        return cls(x, y)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._contains = '.'

    def __str__(self):
        return self.contains

    def __repr__(self):
        return f'({self.x},{self.y},{self.contains})'

    @property
    def point(self):
        return (self.x, self.y)

    @property
    def contains(self):
        return self._contains

    @contains.setter
    def contains(self, value):
        if self._contains == value:
            return
        if self._contains == '#':
            raise ValueError(f'Cannot replace {self._contains} with {value}.')
        self._contains = value

    @property
    def below(self):
        return (self.x, self.y+1)

    @property
    def below_left(self):
        return (self.x-1, self.y+1)

    @property
    def below_right(self):
        return (self.x+1, self.y+1)

    @property
    def is_air(self):
        return bool(self.contains == '.')

    @property
    def is_rock(self):
        return bool(self.contains == '#')


class Map:
    def __init__(self, data):
        self.data = data
        self.rocks = []
        self.sand = Cell(500, 0)
        self.max_x = 500
        self.min_x = 500
        self.max_y = 0
        self.min_y = 0
        self.sand_count = 0

        for row in data:
            bits = row.split(' -> ')
            rocks = [Cell.from_string(bit) for bit in bits]
            self.rocks.append(rocks)

        # Loop over every rock, find the min and max for x and y dimensions.
        for cell in itertools.chain(*self.rocks):
            self.max_x = max(self.max_x, cell.x)
            self.min_x = min(self.min_x, cell.x)
            self.max_y = max(self.max_y, cell.y)
            self.min_y = min(self.min_y, cell.y)

        self.min_x -= 200
        self.max_x += 200
        self.min_y -= 3
        self.max_y += 2

        # Fill in the map with air.
        self.cells_map = dict()

        # Build rows for rendering.
        self.rows = []
        for y in range(self.min_y, self.max_y+1):
            # Build a row
            row = [Cell(x, y) for x in range(self.min_x, self.max_x+1)]
            # Update a map
            self.cells_map.update({cell.point: cell for cell in row})
            self.rows.append(row)

        # Build lines of rocks.
        for rock_line in self.rocks:
            for i, end_rock in enumerate(rock_line[1:], start=1):
                # Rock lines are sequential pairs.
                start_rock = rock_line[i-1]
                x_step = -1 if (start_rock.x > end_rock.x-1) else 1
                y_step = -1 if (start_rock.y > end_rock.y-1) else 1
                for x in range(start_rock.x, end_rock.x+x_step, x_step):
                    for y in range(start_rock.y, end_rock.y+y_step, y_step):
                        self.cells_map[(x, y)].contains = '#'

        # Build the floor.
        for x in range(self.min_x, self.max_x+1):
            self.cells_map[(x, self.max_y)].contains = '#'

        self.cells_map[(500, 0)].contains = '+'

    def __str__(self):
        lines = []
        lines.append('-'*79)
        #lines.append(f'Dimensions: UL to LR ({self.min_x}, {self.min_y}) to ({self.max_x}, {self.max_y})')
        for row in self.rows:
            lines.append(''.join(cell.contains for cell in row))
        return '\n'.join(lines)

    def drop_sand(self):
        sand = Cell(500, 0)
        self.cells_map[sand.point].contains = 'o'
        while True:
            #print(self)
            #time.sleep(0.07)
            # Drop sand until it either comes to rest or falls past the bottom of the map.
            #print(f'Sand is at {repr(sand)}')

            try:
                below = self.cells_map[sand.below]
            except KeyError:
                #print('Sand fell into the void.')
                self.remove_sand(sand)
                return False

            # Part 1, when sand hits the floor, we're done.
            #if self.is_sand_on_floor(sand):
            #    return False

            if below.is_air:
                self.move_down(sand)
                # check bottom before continuing.
                #print(f'Below is air, moving sand to {repr(sand)}.')
                continue

            below_left = self.cells_map[sand.below_left]
            if below_left.is_air:
                self.move_down_left(sand)
                #print(f'Below left is air, moving sand to {repr(sand)}.')
                # We hit something, no need to check bottom yet.
                continue

            below_right = self.cells_map[sand.below_right]
            if below_right.is_air:
                self.move_down_right(sand)
                #print(f'Below right is air, moving sand to {repr(sand)}.')
                # We hit something, no need to check bottom yet.
                continue

            self.sand_count += 1
            if sand.x == 500 and sand.y == 0:
                print('Sand can no longer fall.')
                return False
            # We couldn't move left or right, so we fill the current cell with sand.
            #print(f'Sand can no fall any further.')
            self.cells_map[sand.point].contains = 'o'
            return True

    def move_down(self, sand):
        #print(f'Making {sand.point} air.')
        self.cells_map[sand.point].contains = '.'
        sand.y += 1
        #print(f'Making {sand.point} sand.')
        self.cells_map[sand.point].contains = 'o'

    def move_down_left(self, sand):
        self.cells_map[sand.point].contains = '.'
        sand.x -= 1
        sand.y += 1
        self.cells_map[sand.point].contains = 'o'

    def move_down_right(self, sand):
        self.cells_map[sand.point].contains = '.'
        sand.x += 1
        sand.y += 1
        self.cells_map[sand.point].contains = 'o'

    def remove_sand(self, sand):
        self.cells_map[sand.point].contains = '.'

    def is_sand_on_floor(self, sand):
        if sand.y+1 == self.max_y:
            return True


def part_1(data):
    debug('== Part 1 ==')
    map = Map(data)
    while map.drop_sand():
        pass
    print(map)
    print(f'Sand count: {map.sand_count}')


def part_2(data):
    debug('== Part 2 ==')
    map = Map(data)
    while map.drop_sand():
        pass
    print(map)
    print(f'Sand count: {map.sand_count}')


def main(data):
    INPUT = [
        '498,4 -> 498,6 -> 496,6',
        '503,4 -> 502,4 -> 502,9 -> 494,9',
    ]
    #part_1(data)
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)

