#!/usr/bin/env python3

import collections
import logging
import math
import pathlib
import re


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
    pattern = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')

    sum = 0

    for row in data:
        found = pattern.findall(row)

        for x, y in found:
            x = int(x)
            y = int(y)
            xy = x * y
            print(f'{x} * {y} = {xy}')
            sum += xy

    print(f'Sum: {sum}')


def part_2(data):
    p('== Part 2 ==')
    pattern = re.compile(
        r'''
        (mul)\((\d{1,3}),(\d{1,3})\) |
        (do)\(\) |
        (don't)\(\)
        ''',
        re.VERBOSE
    )

    sum = 0
    enabled = True
    for row in data:
        found = pattern.findall(row)

        for mul, x, y, do, dont in found:
            print(mul, x, y, do, dont)
            if mul and enabled:
                x = int(x)
                y = int(y)
                xy = x * y
                print(f'{x} * {y} = {xy}')
                sum += xy
            elif do:
                enabled = True
            elif dont:
                enabled = False

    print(sum)

def main(data):
    # part_1(data)
    part_2(data)


if __name__ == '__main__':
    data = load_data()
    # data = ['xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))']
    # data = ["""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""]
    main(data)
