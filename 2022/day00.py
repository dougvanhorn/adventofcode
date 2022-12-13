#!/usr/bin/env python3

import collections
import math
import logging
import pathlib

logging.basicConfig(level=logging.ERROR, format='%(message)s')


def debug(message):
    log = logging.getLogger('aoc')
    log.debug(message)


def part_1(data):
    debug('== Part 1 ==')
    pass


def part_2(data):
    debug('== Part 2 ==')
    pass


def main(data):
    part_1(data)
    part_2(data)


if __name__ == '__main__':
    stem = pathlib.Path(__file__).stem
    # Name your input file after this file.
    # E.g., day00input.txt
    with open(f'{stem}input.txt', mode='r+') as fp:
        data = [line.strip() for line in fp.readlines()]

    main(data)

