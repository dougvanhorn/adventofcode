#!/usr/bin/env python3

import collections
import math
import pathlib
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/11


class Cell:
    def __init__(self, row=None, col=None, value=None):
        self.row = row
        self.col = col
        self.value = value

    def __str__(self):
        return f'({self.row}, {self.col}): {self.value}'

    def __repr__(self):
        return self.__str__()

    @property
    def id(self):
        return (self.row, self.col)

    def format_cell(self):
        s = f'{self.value:>2}'
        if self.value == 0:
            return aoc.format(s, "red")
        else:
            return s


class Grid:

    def __init__(self, lines):
        self.lines = lines
        self.cells = []
        # Lookup cells by id.
        self.cell_db = {}
        for row, line in enumerate(lines):
            cell_row = []
            for col, value in enumerate(line):
                cell = Cell(row=row, col=col, value=int(value))
                cell_row.append(cell)
                self.cell_db[cell.id] = cell
            self.cells.append(cell_row)

        self.MAX_ROWS = len(self.cells)
        self.MAX_COLS = len(self.cells[0])

        self.populate_neighbors()

    def print_grid(self):
        rows = []
        for i, row in enumerate(self.cells):
            values = []
            for cell in row:
                values.append(cell.format_cell())
            col = ' '.join(values)
            rows.append(f'{i:>02}: {col}')
        print('\n'.join(rows))

    def iterate_cells(self):
        # Loop over rows, cells as a generator.
        for row in self.cells:
            for cell in row:
                yield cell

    def populate_neighbors(self):
        # Append a list of neighbors to each cell.
        for cell in self.iterate_cells():
            row, col = cell.id
            moves = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1),
            ]
            neighbors = []
            for row_delta, col_delta in moves:
                neighbor_id = (row + row_delta, col + col_delta)
                neighbor_cell = self.cell_db.get(neighbor_id)
                if neighbor_cell:
                    neighbors.append(neighbor_cell)

            cell.neighbors = neighbors

    def run(self):
        # Run the grid.
        # keep track of what we've flashed.
        marked = {}
        # keep track of what needs to be flashed.
        flash_cells = {}
        # keep track of what the flash count is.
        flash_count = 0

        # Step one.
        for cell in self.iterate_cells():
            cell.value += 1

        # flash a cell.
        def flash(cell):
            # Mark the cell so we don't visit it again.
            marked[cell.id] = cell
            # Reset the value to 0.
            cell.value = 0
            # for every neighbor...
            for neighbor in cell.neighbors:
                # skip it if it's marked
                if neighbor.id in marked:
                    continue

                # absorb energy.
                neighbor.value += 1

                # Just crossed the flash threshold, add to the flash list.
                if neighbor.value == 10:
                    flash_cells[neighbor.id] = neighbor

        # Queue up all cells that need to flash.
        for cell in self.iterate_cells():
            if cell.value >= 10:
                flash_cells[cell.id] = cell

        # keep flashing cells until we've no more to flash.
        while flash_cells:
            # FIFO
            first_key = list(flash_cells.keys())[0]
            cell = flash_cells.pop(first_key)
            flash_count += 1
            flash(cell)

        # special case, if all neighbors flashed then i need to flash.
        unflashed_cells = [c for c in self.iterate_cells() if cell.value > 0]
        for cell in unflashed_cells:
            values = [n.value for n in cell.neighbors]
            # if all my neighbor values sum to 0...
            if sum(values) == 0:
                # then i need to flash too.
                flash_count += 1
                cell.value = 0

        return flash_count


def part_1(input_lines):
    grid = Grid(input_lines)

    print('Round 0')
    grid.print_grid()

    flash_count = 0

    for round in range(1, 101):
        flashes = grid.run()
        flash_count += flashes
        if (round % 10) == 0:
            print(f'Round {round}')
            grid.print_grid()
            print()

    print('flash count', flash_count)


def part_2(input_lines):
    grid = Grid(input_lines)

    print('Round 0')
    grid.print_grid()

    for round in range(1, 1001):
        flashes = grid.run()
        if (round % 10) == 0:
            print(f'Round {round}')
            grid.print_grid()
            print()
        if flashes == 100:
            print(f'flashes == 100 in round {round}')
            break


def main(input_lines):
    print('Part 1')
    print('=' * 79)
    part_1(input_lines)
    print()
    print()
    print('Part 2')
    print('=' * 79)
    part_2(input_lines)


TEST_INPUT = [
    '5483143223',
    '2745854711',
    '5264556173',
    '6141336146',
    '6357385478',
    '4167524645',
    '2176841721',
    '6882881134',
    '4846848554',
    '5283751526',
]

if __name__ == '__main__':
    path = pathlib.Path(__file__)
    day_number = path.name[3:5]
    filename = f'{day_number}.txt'
    lines = aoc.loadfile(filename)
    _lines = TEST_INPUT
    n = len(lines)
    aoc.format(f'Loaded {filename}: {n} lines.', 'blue')
    main(lines)
