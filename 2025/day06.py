#!/usr/bin/env python

import collections
import logging
import math
import pathlib

import rich
from rich.progress import track


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger('aoc')


def load_data():
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00-input.txt
    with open(f'{stem}-input.txt', mode='r+') as fp:
        data = [line.strip('\n') for line in fp.readlines()]
    return data


def part_1(data):
    rich.print('[bold red]== Part 1 ==[/bold red]')
    rich.print('Group by columns, perform calculations.')

    rows = [row.split() for row in data]
    groups = zip(*rows)
    calculators = [Calculator(group) for group in groups]

    answer = sum(calc.calculate() for calc in calculators)
    rich.print(f'[bold green]Answer: {answer}[/bold green]')


def part_2(data):
    rich.print('[bold red]== Part 2 ==[/bold red]')
    rich.print('Group by columns, read columns top to bottom perform calculations.')

    # for row in data:
    #     print(f'length: "{len(row)}"')

    # Determine column sizes first, use last row.
    # Operator index indicates the first column position.
    indexes = [i for i in range(len(data[-1])) if data[-1][i] in ('+', '*')]
    # print(f'Indexes: {indexes}')
    # Add end index.
    indexes.append(len(data[-1])+1)

    widths = [
        slice(indexes[i], indexes[i+1]-1)
        for i in range(len(indexes)-1)
    ]
    slices = []
    # for width in widths:
    #     slices.append(f'[{width.start}:{width.stop}]')
    # print(f'Widths: {slices}')

    rows = []
    for row in data:
        columns = [
            row[width]
            for width in widths
        ]
        # print(f'  Columns: {columns}')
        rows.append(columns)

    # Group into problems.
    groups = list(zip(*rows))
    # print('Groups of problems:')
    # print(groups)

    cephulators = [Cephulator(group) for group in groups]
    answer = sum(ceph.calculate() for ceph in cephulators)
    rich.print(f'[bold green]Answer: {answer}[/bold green]')

    cephulators[-1].debug()


class Cephulator:
    def __init__(self, data):
        self.data = data
        self.original_numbers = [x for x in data[:-1]]
        self.operator = data[-1].strip()

        # e.g., ['123', ' 45', '  6']
        # We need to read right to left, top to bottom.
        # Strings are fixed width, so spaces are in the right spots.
        # Reverse the strings.  e.g., ['321', '54 ', '6  ']
        r2l_numbers = [x[::-1] for x in self.original_numbers]
        # Zip, e.g., [('3','5','6'), ('2','4',' '), ('1',' ',' ')]
        top2bottom_numbers = list(zip(*r2l_numbers))
        # intify, e.g., [356, 24, 1]
        self.numbers = [
            int(''.join(num))
            for num in top2bottom_numbers
        ]

    def calculate(self):
        if self.operator == '+':
            return sum(self.numbers)
        elif self.operator == '*':
            return math.prod(self.numbers)
        else:
            raise ValueError(f'Unknown operator: {self.operator}')

    def debug(self):
        print(f'Original numbers: {self.original_numbers}')
        print(f'Parsed numbers:   {self.numbers}')
        print(f'Operator:         {self.operator}')
        print(f'Calculation:      {self.calculate()}')


class Calculator:
    def __init__(self, data):
        self.data = data
        self.numbers = [int(x) for x in data[:-1]]
        self.operator = data[-1]

    def calculate(self):
        if self.operator == '+':
            return sum(self.numbers)
        elif self.operator == '*':
            return math.prod(self.numbers)
        else:
            raise ValueError(f'Unknown operator: {self.operator}')


def main(data):
    _data = [
        '123 328  51 64 ',
        ' 45 64  387 23 ',
        '  6 98  215 314',
        '*   +   *   +  ',
    ]
    # part_1(data)
    part_2(data)


if __name__ == '__main__':
    data = load_data()
    main(data)
