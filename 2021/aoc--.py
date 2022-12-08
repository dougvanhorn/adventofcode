#!/usr/bin/env python3

import collections
import math
import pathlib
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/-


def part_1(input_lines):
    print(aoc.format('Part 1 not implemented.', 'red'))


def part_2(input_lines):
    print(aoc.format('Part 2 not implemented.', 'red'))


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

]


if __name__ == '__main__':
    path = pathlib.Path(__file__)
    day_number = path.name[3:5]
    filename = f'{day_number}.txt'
    lines = aoc.loadfile(filename)
    lines = TEST_INPUT
    n = len(lines)
    print(aoc.format(f'Loaded {filename}: {n} lines.', 'blue'))
    main(lines)
