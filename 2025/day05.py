#!/usr/bin/env python

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


def part_1(data):
    p('== Part 1 ==')
    pass


def part_2(data):
    p('== Part 2 ==')
    pass


def main(data):
    _data = [
    ]
    # part_1(data)
    # part_2(data)


if __name__ == '__main__':
    data = load_data()
    main(data)
