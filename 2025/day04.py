#!/usr/bin/env python

import collections
import dataclasses
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


@dataclasses.dataclass
class Cell:
    row: int
    col: int
    value: str

class Grid:
    def __init__(self, data):
        self.grid = data
        self.row_count = len(data)
        self.col_count = len(data[0])
        print(f'Grid initialized: {self.row_count} rows, {self.col_count} cols')
        print(f'  Size: {self.row_count * self.col_count}')

        self.paper_count = len([cell for cell in self.cell_iter() if cell.value == '@'])
        self.empty_count = len([cell for cell in self.cell_iter() if cell.value == '.'])
        print(f'Paper count: {self.paper_count}, Empty count: {self.empty_count}')

        self.paper_locations = {
            (cell.row, cell.col): cell
            for cell in self.cell_iter()
            if cell.value == '@'
        }

    def cell_iter(self):
        for row in range(self.row_count):
            for col in range(self.col_count):
                yield Cell(row, col, self.grid[row][col])

    def is_moveable(self, cell):
        neighbors = self.neighbors(cell)
        return len(neighbors) < 4

    def neighbors(self, cell):
        deltas = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        neighbors = []
        for delta_row, delta_col in deltas:
            check_row, check_col = cell.row + delta_row, cell.col + delta_col
            neighbor_cell = self.paper_locations.get((check_row, check_col), None)
            if neighbor_cell is None:
                continue
            if neighbor_cell.value == '@':
                neighbors.append(neighbor_cell)
        return neighbors

    def get_cell(self, row, col):
        # If we're out of bounds, return None.
        if not (0 <= row < self.row_count):
            return None
        if not (0 <= col < self.col_count):
            return None

        return Cell(row, col, self.grid[row][col])


def part_1(data):
    """Check for moveable rolls of paper.

    Roll is moveable if neighbors < 4
    """
    p('== Part 1 ==')
    grid = Grid(data)

    moveable_rolls = 0

    for cell in grid.paper_locations.values():
        if cell.value != '@':
            continue

        neighbors = grid.neighbors(cell)

        if len(neighbors) < 4:
            # print(f'  {cell} has {len(neighbors)} neighbors.  Moveable Roll Found')
            moveable_rolls+= 1
        else:
            pass
            # print(f'  {cell} has {len(neighbors)} neighbors.')

    print(f'Total rolls found: {moveable_rolls}')


def part_2(data):
    """Check for moveable rolls of paper.

    Roll is moveable if neighbors < 4

    Continue removing rolls until no more can be removed.
    """
    p('== Part 2 ==')
    grid = Grid(data)

    count = 0

    removeable = [cell for cell in grid.paper_locations.values() if grid.is_moveable(cell)]
    # print(f'found {len(removeable)} removeable rolls')
    for cell in removeable:
        del grid.paper_locations[(cell.row, cell.col)]
    count += len(removeable)

    while removeable:
        # print(f'{len(grid.paper_locations)} rolls remain')
        removeable = [cell for cell in grid.paper_locations.values() if grid.is_moveable(cell)]
        # print(f'found {len(removeable)} removeable rolls')
        for cell in removeable:
            del grid.paper_locations[(cell.row, cell.col)]
        count += len(removeable)

    print(f'Total rolls found {count}')


def main(data):
    _data = [
        '..@@.@@@@.',
        '@@@.@.@.@@',
        '@@@@@.@.@@',
        '@.@@@@..@.',
        '@@.@@@@.@@',
        '.@@@@@@@.@',
        '.@.@.@.@@@',
        '@.@@@.@@@@',
        '.@@@@@@@@.',
        '@.@.@@@.@.',
    ]
    part_1(data)
    part_2(data)


if __name__ == '__main__':
    data = load_data()
    main(data)
