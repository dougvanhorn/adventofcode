#!/usr/bin/env python3

import collections
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


def part_1(left_list, right_list):
    # Sum the absolute difference between the two lists.
    p('== Part 1 ==')
    left_list.sort()
    right_list.sort()

    delta = 0
    for left, right in zip(left_list, right_list):
        delta += abs(left - right)

    p(f'Total difference: {delta}')


def part_2(left_list, right_list):
    # Build count in right list, use as multiplier.
    p('== Part 2 ==')

    delta = 0
    counts = collections.Counter(right_list)
    for left in left_list:
        # p(f'Left: {left}, Count: {counts[left]}, Product: {left * counts[left]}')
        count = counts[left]
        product = left * count
        delta += product

    print(f'Total difference: {delta}')


def main(_input):
    left_list = []
    right_list = []

    for row in _input:
        left, right = row.split()
        left_list.append(int(left))
        right_list.append(int(right))

    # part_1(left_list, right_list)
    part_2(left_list, right_list)


if __name__ == '__main__':
    data = load_data()
    _data = [
        '3   4',
        '4   3',
        '2   5',
        '1   3',
        '3   9',
        '3   3',
    ]
    main(data)
