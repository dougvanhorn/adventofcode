#!/usr/bin/env python3

import collections
import itertools
import math
import re
import traceback

import aoc

class Row:
    def __init__(self, line_number, value):
        self.line_number

class Cipher:
    def __init__(self, lines):
        self.lines = lines
        self.preamble_size = 25

        self.sums = collections.defaultdict(list)
        for i, x in enumerate(self.lines[:25]):
            self.sums[(i, int(x))] = []

        self.current_line = 25


def main():
    lines = aoc.loadfile('09.txt')
    lines = [int(line) for line in lines]
    print(f'{len(lines)} lines.')

    cipher = Cipher(lines)

    invalid_num = 542529149

    less_than = [line for line in lines if line < invalid_num]
    print('less than', len(less_than))
    i = 0
    j = 1
    while j < len(lines):
        current_sum = sum(lines[i:j+1])
        print(f'checking [{i}:{j}]: {current_sum} ? {invalid_num}')
        if current_sum == invalid_num:
            print(f'found [{i}:{j+1}]: {lines[i:j+1]}')
            smallest = min(lines[i:j+1])
            largest = max(lines[i:j+1])
            print(f'{smallest} + {largest} = {smallest + largest}')
            return
        elif current_sum < invalid_num:
            j += 1
        else:
            i += 1
            j = max(i+1, j)

    return 'not found'

    i = 0
    j = 25

    weak = []

    for value_i, value in enumerate(lines[25:], start=25):
        combos = list(itertools.combinations(lines[i:j], 2))
        sums = {sum(tpl) for tpl in combos}
        print(f'Checking line[{value_i}]: {value} in lines[{i}:{j}], {len(combos)} Combos, {len(sums)} sums.')
        if value not in sums:
            weak.append((value_i, value))
            print(f'Adding {lines[value_i]} as weakness.')

        i += 1
        j += 1

    print(weak)


if __name__ == '__main__':
    main()
