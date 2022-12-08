#!/usr/bin/env python3

import collections
import math
import pathlib
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/13

class Cell:
    def __init__(self, row, col, value='.'):
        self.row = row
        self.col = col
        self.value = value
        self.default = '.'

    @property
    def id(self):
        return (self.row, self.col)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'[({self.row}, {self.col}), {self.value}]'

    def pformat(self):
        if self.value == self.default:
            return self.default
        else:
            return aoc.format(self.value, 'bold red')

class Fold:
    def __init__(self, axes, value):
        self.axes = axes
        self.is_x = (axes == 'x')
        self.is_y = (axes == 'y')
        self.value = value

    def __str__(self):
        return f'Fold along {self.axes}={self.value}'


class Paper:
    def __init__(self, lines):
        self.lines = lines

        self.points = []
        # Lookup by coord.
        self.points_db = {}

        self.folds = collections.deque()

        for line in lines:
            if ',' in line:
                # x increases right, y increases down
                x, y = map(int, line.split(','))
                cell = Cell(y, x, value='#')
                self.points.append(cell)
                self.points_db[cell.id] = cell

            elif line.startswith('fold'):
                axes = line[11]
                value = int(line[13:])
                self.folds.append(Fold(axes, value))

        self.MAX_ROWS = max(cell.row for cell in self.points)
        self.MAX_COLS = max(cell.col for cell in self.points)

    def print_info(self):
        max_rows = max(cell.row for cell in self.points_db.values())
        max_cols = max(cell.col for cell in self.points_db.values())
        print('='*79)
        print('Paper Info')
        print('-'*79)
        print(f'Rows: {max_rows}')
        print(f'Cols: {max_cols}')
        print(f'Points: {len(self.points_db)}')
        print('Folds:')
        for fold in self.folds:
            print(f'  {fold}')

        row_strings = []
        for row in range(max_rows+1):
            row_string = collections.deque()
            for col in range(max_cols+1):
                if (row, col) in self.points_db:
                    row_string.append('#')
                else:
                    row_string.append('.')
            row_strings.append(''.join(s for s in row_string))
        print('Grid:')
        print('\n'.join(row_strings))
        print('-'*79)

    def fold(self):
        fold = self.folds.popleft()
        if fold.is_x:
            self.fold_x(fold)
        else:
            self.fold_y(fold)

    def fold_x(self, fold):
        print(f'### Folding {fold}')
        # invert the right half to the left
        fold_col = fold.value
        right_of_fold = [cell for cell in self.points_db.values() if cell.col > fold_col]
        for cell in right_of_fold:
            fold_delta = cell.col - fold_col
            new_col = fold_col - fold_delta
            del self.points_db[cell.id]
            cell.col = new_col
            self.points_db.setdefault(cell.id, cell)

    def fold_y(self, fold):
        print(f'### Folding {fold}')
        # invert the bottom half to the top half.
        fold_row = fold.value
        below_fold = [cell for cell in self.points_db.values() if cell.row > fold_row]
        for cell in below_fold:
            fold_delta = cell.row - fold_row
            new_row = fold_row - fold_delta
            del self.points_db[cell.id]
            cell.row = new_row
            self.points_db.setdefault(cell.id, cell)


def part_1(input_lines):
    paper = Paper(input_lines)
    paper.print_info()
    paper.fold()
    paper.print_info()


def part_2(input_lines):
    paper = Paper(input_lines)
    while paper.folds:
        paper.fold()
    paper.print_info()


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
    '6,10',
    '0,14',
    '9,10',
    '0,3',
    '10,4',
    '4,11',
    '6,0',
    '6,12',
    '4,1',
    '0,13',
    '10,12',
    '3,4',
    '3,0',
    '8,4',
    '1,10',
    '2,14',
    '8,10',
    '9,0',
    '',
    'fold along y=7',
    'fold along x=5',
]

if __name__ == '__main__':
    path = pathlib.Path(__file__)
    day_number = path.name[3:5]
    filename = f'{day_number}.txt'
    lines = aoc.loadfile(filename)
    _lines = TEST_INPUT
    n = len(lines)
    print(aoc.format(f'Loaded {filename}: {n} lines.', 'blue'))
    main(lines)
