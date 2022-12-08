#!/usr/bin/env python3

import collections
import math
import pprint
import re
import traceback

import aoc


def main():
    raw_lines = aoc.loadfile('01.txt')

    lines = [int(line) for line in raw_lines]

    last_depth = lines[0]
    increased = 0
    for i, depth in enumerate(lines[1:]):
        if depth - last_depth > 0:
            increased += 1
        last_depth = depth

    print('increases', increased)

    increased = 0
    previous_sum = sum(lines[:3])
    for i in range(2, len(lines)):
        current_sum = sum(lines[i-2:i+1])
        print(f'{current_sum} > {previous_sum}')
        if current_sum > previous_sum:
            increased += 1
        previous_sum = current_sum

    print('window increases', increased)


if __name__ == '__main__':
    main()
