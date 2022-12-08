#!/usr/bin/env python3

import collections
import math
import pprint
import re
import traceback

import aoc


# https://adventofcode.com/2021/day/3


def main():
    lines = aoc.loadfile('03.txt')

    gamma = ''  # most common
    epsilon = ''  # least common
    
    n_lines = len(lines)
    over_under = n_lines / 2

    # =========================================================================
    # Part 1
    # -------------------------------------------------------------------------
    # Loop over all lines and keep a running sum for each column.
    # If the column > 1/2 the number of lines then ones are more common.

    # A place to store our columnar sums.
    sums = [0] * len(lines[0])
    for line in lines:
        # keep a running total of each 12 positions
        for i, bit in enumerate(line):
            sums[i] += int(bit)

    for column_total in sums:
        if column_total > over_under:
            gamma += '1'
            epsilon += '0'
        elif column_total < over_under:
            gamma += '0'
            epsilon += '1'
        else:
            raise Exception(f'column_total == over_under: {column_total} == {over_under}')

    gamma_decimal = int(gamma, base=2)
    epsilon_decimal = int(epsilon, base=2)

    print(f'gamma: {gamma}')
    print(f'gamma_decimal: {gamma_decimal}')
    print(f'epsilon: {epsilon}')
    print(f'epsilon_decimal: {epsilon_decimal}')
    print(f'power consumption: {gamma_decimal * epsilon_decimal}')
    # -------------------------------------------------------------------------

    # =========================================================================
    # Part 2
    # -------------------------------------------------------------------------
    # Filter lines until we have one winner for each reading type.

    def filter_lines(lines, position, reading_type):
        """Given a set of lines and a position to looko at, filter the lines.

        For o2, keep the line if it's nth position sum is more than or equal to half.
        For co2, keep the line if it's nth position sum is less than or equal to half.
        """
        n_lines = len(lines)
        # sum the nth position
        column_total = sum([int(line[position]) for line in lines])
        # 1s
        ones = column_total
        # 0s
        zeros = n_lines - ones

        if ones > zeros:
            bit_value_to_keep = '1' if reading_type == 'o2' else '0'

        elif ones < zeros:
            bit_value_to_keep = '0' if reading_type == 'o2' else '1'

        else:
            # Equal, tie break on reading type.
            bit_value_to_keep = '1' if reading_type == 'o2' else '0'

        filtered_lines = [line for line in lines if line[position] == bit_value_to_keep]
        return filtered_lines

    o2_lines = list(lines)
    for column, _ in enumerate(lines[0]):
        if len(o2_lines) == 1:
            break
        o2_lines = filter_lines(o2_lines, column, 'o2')

    if len(o2_lines) != 1:
        print(f'bad filtered o2 lines. {o2_lines}')
    else:
        o2 = int(o2_lines[0], base=2)

    co2_lines = list(lines)
    for column, _ in enumerate(lines[0]):
        if len(co2_lines) == 1:
            break
        co2_lines = filter_lines(co2_lines, column, 'co2')

    if len(o2_lines) != 1:
        print(f'bad filtered co2 lines. {co2_lines}')
    else:
        co2 = int(co2_lines[0], base=2)

    print(f'o2: {o2}')
    print(f'co2: {co2}')
    print(f'life support: {o2 * co2}')
    # -------------------------------------------------------------------------


if __name__ == '__main__':
    main()
