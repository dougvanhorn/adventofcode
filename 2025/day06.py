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
        data = [line.strip() for line in fp.readlines()]
    return data


def part_1(data):
    rich.print('[bold red]== Part 1 ==[/bold red]')
    rich.print('description')
    pass


def part_2(data):
    rich.print('[bold red]== Part 2 ==[/bold red]')
    rich.print('description')
    pass


def main(data):
    _data = [

    ]
    # part_1(data)
    # part_2(data)


if __name__ == '__main__':
    data = load_data()
    main(data)
